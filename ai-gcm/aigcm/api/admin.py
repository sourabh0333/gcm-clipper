"""Owner-only routes. M2: the beta invite list."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from ..db.models import AuditEntry, Invite
from .deps import admin_user, get_db

router = APIRouter(prefix="/api/admin")


class NewInvite(BaseModel):
    email: str


@router.get("/invites")
def list_invites(user=Depends(admin_user), db=Depends(get_db)):
    return [{"email": i.email, "created_at": i.created_at.isoformat()} for i in db.scalars(select(Invite))]


@router.post("/invites", status_code=201)
def add_invite(body: NewInvite, user=Depends(admin_user), db=Depends(get_db)):
    email = body.email.strip().lower()
    if "@" not in email or len(email) > 320:
        raise HTTPException(400, "That doesn't look like an email address.")
    if db.get(Invite, email) is None:
        db.add(Invite(email=email, invited_by=user.id))
        db.add(AuditEntry(user_id=user.id, action="invite", detail={"email": email}))
        db.commit()
    return {"email": email}


@router.delete("/invites/{email}")
def remove_invite(email: str, user=Depends(admin_user), db=Depends(get_db)):
    invite = db.get(Invite, email.lower())
    if invite is None:
        raise HTTPException(404, "Not found.")
    db.delete(invite)
    db.add(AuditEntry(user_id=user.id, action="uninvite", detail={"email": email.lower()}))
    db.commit()
    return {"ok": True}
