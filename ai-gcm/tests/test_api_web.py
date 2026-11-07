"""The API serves the built web app, and never lets the app's fallback swallow API paths."""

import pytest
from fastapi.testclient import TestClient

from aigcm import db
from aigcm.api import create_app
from aigcm.api.settings import ApiSettings


@pytest.fixture
def dist(tmp_path):
    d = tmp_path / "dist"
    (d / "assets").mkdir(parents=True)
    (d / "index.html").write_text("<div id=root></div>")
    (d / "sw.js").write_text("// sw")
    (d / "assets" / "index-abc123.js").write_text("console.log(1)")
    return d


def make(tmp_path, web_dir):
    return TestClient(create_app(ApiSettings(db_url=db.sqlite_url(tmp_path / "t.db"), jobs_dir=tmp_path / "jobs",
                                             web_dir=web_dir)))


def test_pages_files_and_assets(tmp_path, dist):
    client = make(tmp_path, dist)
    for path in ("/", "/streams/st_1", "/kept", "/streams/st_1/review"):
        page = client.get(path)
        assert page.status_code == 200 and "root" in page.text and page.headers["cache-control"] == "no-cache"
    assert client.get("/sw.js").text == "// sw"
    assert client.get("/assets/index-abc123.js").status_code == 200


def test_api_paths_never_fall_back_to_the_app(tmp_path, dist):
    client = make(tmp_path, dist)
    assert client.get("/api/nothing-here").status_code == 404
    assert client.get("/media/clips/1").status_code in (401, 404)
    assert client.get("/auth/nothing").status_code == 404
    assert client.get("/api/health").json()["ok"] is True


def test_path_tricks_get_the_app_not_files(tmp_path, dist):
    (tmp_path / "secret.txt").write_text("secret")
    client = make(tmp_path, dist)
    for path in ("/..%2fsecret.txt", "/%2e%2e/secret.txt", "/assets/../../secret.txt"):
        response = client.get(path)
        assert "secret" not in response.text


def test_an_unbuilt_app_explains_itself(tmp_path):
    response = make(tmp_path, tmp_path / "nothing").get("/")
    assert response.status_code == 503 and "npm run build" in response.text
