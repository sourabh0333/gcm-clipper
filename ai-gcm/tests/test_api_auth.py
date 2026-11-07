"""Sign-in, sessions, invites, the cross-site guard and per-user access, against a fake Google."""

import datetime as dt
import json
import time
from urllib.parse import parse_qs, urlparse

import httpx
import pytest
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from fastapi.testclient import TestClient
from google.auth import crypt
from google.auth import jwt as google_jwt

from aigcm import db
from aigcm.api import create_app
from aigcm.api.auth import CERTS_URL, TOKEN_URL, safe_next
from aigcm.api.settings import ApiSettings
from aigcm.db.models import Session as SessionRow
from aigcm.db.models import Stream, User

CLIENT_ID = "test-client.apps.googleusercontent.com"
APP = {"x-kaatclip": "1"}


def make_key():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "fake google")])
    now = dt.datetime.now(dt.UTC)
    cert = (x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key())
            .serial_number(1).not_valid_before(now - dt.timedelta(days=1)).not_valid_after(now + dt.timedelta(days=1))
            .sign(key, hashes.SHA256()))
    pem = key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
    return pem, cert.public_bytes(serialization.Encoding.PEM).decode()


KEY_PEM, CERT_PEM = make_key()
OTHER_KEY_PEM, _ = make_key()


class FakeGoogle:
    """Answers the token exchange with an ID token built from `claims`, signed with `key`."""

    def __init__(self):
        self.claims, self.key, self.nonce, self.exchanges = {}, KEY_PEM, None, []

    def handler(self, request: httpx.Request):
        if request.url == CERTS_URL:
            return httpx.Response(200, json={"k1": CERT_PEM}, headers={"cache-control": "public, max-age=3600"})
        if request.url == TOKEN_URL:
            form = parse_qs(request.content.decode())
            self.exchanges.append(form)
            now = int(time.time())
            payload = {"iss": "https://accounts.google.com", "aud": CLIENT_ID, "sub": "g-123",
                       "email": "creator@example.com", "email_verified": True, "name": "Creator",
                       "iat": now, "exp": now + 600, "nonce": self.nonce}
            payload.update(self.claims)
            signer = crypt.RSASigner.from_string(self.key, key_id="k1")
            token = google_jwt.encode(signer, payload, header={"kid": "k1"}).decode()
            return httpx.Response(200, json={"id_token": token, "access_token": "x"})
        return httpx.Response(404)


@pytest.fixture
def google():
    return FakeGoogle()


def build(tmp_path, google, **settings):
    base = dict(db_url=db.sqlite_url(tmp_path / "t.db"), jobs_dir=tmp_path / "jobs", google_client_id=CLIENT_ID,
                google_client_secret="secret", invites=frozenset({"creator@example.com", "second@example.com"}),
                admins=frozenset({"owner@example.com"}))
    base.update(settings)
    return create_app(ApiSettings(**base), http=httpx.Client(transport=httpx.MockTransport(google.handler)))


def sign_in(client, google, next_path="/"):
    start = client.get("/auth/google/start", params={"next": next_path}, follow_redirects=False)
    assert start.status_code == 302
    query = parse_qs(urlparse(start.headers["location"]).query)
    google.nonce = query["nonce"][0]
    return client.get("/auth/google/callback", params={"code": "c0de", "state": query["state"][0]},
                      follow_redirects=False), query


def test_google_sign_in_with_pkce_creates_a_session(tmp_path, google):
    client = TestClient(build(tmp_path, google))
    done, query = sign_in(client, google, "/streams/abc")
    assert query["scope"] == ["openid email profile"] and query["code_challenge_method"] == ["S256"]
    assert done.status_code == 302 and done.headers["location"] == "/streams/abc"
    assert google.exchanges[0]["code_verifier"][0] and google.exchanges[0]["code"] == ["c0de"]
    me = client.get("/api/me").json()
    assert me == {"email": "creator@example.com", "name": "Creator", "picture": None, "admin": False}
    cookie = done.headers["set-cookie"]
    assert "httponly" in cookie.lower() and "samesite=lax" in cookie.lower()


def test_owner_is_admin(tmp_path, google):
    google.claims = {"email": "owner@example.com", "sub": "g-owner"}
    client = TestClient(build(tmp_path, google))
    sign_in(client, google)
    assert client.get("/api/me").json()["admin"] is True


@pytest.mark.parametrize("claims, status", [
    ({"email": "stranger@example.com"}, 403),          # not invited
    ({"email_verified": False}, 403),                  # unverified address
    ({"aud": "someone-else"}, 502),                    # token for another app
    ({"iss": "https://evil.example"}, 502),            # wrong issuer
    ({"nonce": "replayed"}, 502),                      # nonce from another sign-in
    ({"exp": int(time.time()) - 60}, 502),             # expired
])
def test_bad_or_unwelcome_tokens_are_refused(tmp_path, google, claims, status):
    google.claims = claims
    client = TestClient(build(tmp_path, google))
    done, _ = sign_in(client, google)
    assert done.status_code == status
    assert client.get("/api/me").status_code == 401


def test_a_token_signed_by_another_key_is_refused(tmp_path, google):
    google.key = OTHER_KEY_PEM
    client = TestClient(build(tmp_path, google))
    done, _ = sign_in(client, google)
    assert done.status_code == 502 and client.get("/api/me").status_code == 401


def test_state_must_match_the_pending_login(tmp_path, google):
    client = TestClient(build(tmp_path, google))
    start = client.get("/auth/google/start", follow_redirects=False)
    google.nonce = parse_qs(urlparse(start.headers["location"]).query)["nonce"][0]
    wrong = client.get("/auth/google/callback", params={"code": "c", "state": "forged"}, follow_redirects=False)
    assert wrong.status_code == 400
    # Without the pending-login cookie (another browser), the callback is refused too.
    fresh = TestClient(client.app)
    assert fresh.get("/auth/google/callback", params={"code": "c", "state": "x"}).status_code == 400


def test_next_only_goes_to_this_site():
    assert safe_next("/streams/1") == "/streams/1"
    assert safe_next("//evil.com/x") == "/" and safe_next("https://evil.com") == "/" and safe_next(None) == "/"
    assert safe_next("/\\evil.com") == "/" and safe_next("/x\nSet-Cookie: a=b") == "/"


def test_sign_out_kills_the_session_even_if_the_cookie_is_replayed(tmp_path, google):
    client = TestClient(build(tmp_path, google))
    sign_in(client, google)
    token = client.cookies.get("kc_session")
    assert client.post("/auth/logout", headers=APP).status_code == 200
    replay = TestClient(client.app)
    replay.cookies.set("kc_session", token)
    assert replay.get("/api/me").status_code == 401


def test_expired_sessions_and_unknown_tokens_are_signed_out(tmp_path, google):
    app = build(tmp_path, google)
    client = TestClient(app)
    sign_in(client, google)
    with app.state.sessions() as s:
        for row in s.query(SessionRow):
            row.expires_at = row.expires_at - dt.timedelta(days=60)
        s.commit()
    assert client.get("/api/me").status_code == 401
    client.cookies.set("kc_session", "made-up")
    assert client.get("/api/me").status_code == 401


def test_state_changing_calls_need_the_app_header_and_origin(tmp_path, google):
    client = TestClient(build(tmp_path, google))
    sign_in(client, google)
    assert client.post("/auth/logout").status_code == 403
    evil = dict(APP, origin="https://evil.example")
    assert client.post("/auth/logout", headers=evil).status_code == 403
    assert client.get("/api/me").status_code == 200   # still signed in


def test_dev_sign_in_only_on_this_laptop_and_only_when_switched_on(tmp_path, google):
    off = TestClient(build(tmp_path / "a", google), base_url="http://localhost")
    assert off.post("/auth/dev-login", json={"email": "creator@example.com"}, headers=APP).status_code == 404
    app = build(tmp_path / "b", google, dev_login=True)
    remote = TestClient(app)   # host "testserver", as a tunnel would present a public name
    assert remote.post("/auth/dev-login", json={"email": "creator@example.com"}, headers=APP).status_code == 404
    local = TestClient(app, base_url="http://localhost")
    tunnelled = dict(APP, **{"x-forwarded-for": "1.2.3.4"})
    assert local.post("/auth/dev-login", json={"email": "creator@example.com"}, headers=tunnelled).status_code == 404
    assert local.post("/auth/dev-login", json={"email": "stranger@example.com"}, headers=APP).status_code == 403
    assert local.post("/auth/dev-login", json={"email": "creator@example.com"}, headers=APP).status_code == 200
    assert local.get("/api/me").json()["email"] == "creator@example.com"
    assert local.get("/api/auth-config").json() == {"google": True, "dev": True}


def test_creators_only_see_their_own_streams(tmp_path, google):
    app = build(tmp_path, google, dev_login=True)
    a, b = (TestClient(app, base_url="http://localhost") for _ in range(2))
    a.post("/auth/dev-login", json={"email": "creator@example.com"}, headers=APP)
    b.post("/auth/dev-login", json={"email": "second@example.com"}, headers=APP)
    with app.state.sessions() as s:
        owner = s.query(User).filter_by(email="creator@example.com").one()
        stream = Stream(user_id=owner.id, title="Rank push", job_dir="st_a")
        s.add(stream)
        s.commit()
        stream_id = stream.id
    assert [x["id"] for x in a.get("/api/streams").json()] == [stream_id]
    assert a.get(f"/api/streams/{stream_id}").status_code == 200
    assert b.get("/api/streams").json() == []
    assert b.get(f"/api/streams/{stream_id}").status_code == 404
    assert TestClient(app).get("/api/streams").status_code == 401


def test_only_admins_manage_invites_and_an_invite_lets_someone_in(tmp_path, google):
    app = build(tmp_path, google, dev_login=True)
    owner, creator = (TestClient(app, base_url="http://localhost") for _ in range(2))
    owner.post("/auth/dev-login", json={"email": "owner@example.com"}, headers=APP)
    creator.post("/auth/dev-login", json={"email": "creator@example.com"}, headers=APP)
    assert creator.post("/api/admin/invites", json={"email": "new@example.com"}, headers=APP).status_code == 403
    assert owner.post("/api/admin/invites", json={"email": "New@Example.com"}, headers=APP).status_code == 201
    assert [i["email"] for i in owner.get("/api/admin/invites").json()] == ["new@example.com"]
    newcomer = TestClient(app, base_url="http://localhost")
    assert newcomer.post("/auth/dev-login", json={"email": "new@example.com"}, headers=APP).status_code == 200


def test_google_start_explains_when_not_set_up(tmp_path, google):
    client = TestClient(build(tmp_path, google, google_client_id=""))
    response = client.get("/auth/google/start", follow_redirects=False)
    assert response.status_code == 503 and "GOOGLE_CLIENT_ID" in response.json()["detail"]


def test_cookies_are_secure_over_https(tmp_path, google):
    client = TestClient(build(tmp_path, google), base_url="https://kc.example")
    done, _ = sign_in(client, google)
    assert "secure" in done.headers["set-cookie"].lower()
