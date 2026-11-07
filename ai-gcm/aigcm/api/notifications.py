"""Connecting Telegram from Settings (see aigcm/telegram.py for the bot side)."""

from fastapi import APIRouter, Depends, HTTPException, Request

from ..db.models import TelegramLink
from ..telegram import new_link_token
from .deps import current_user, get_db

router = APIRouter(prefix="/api/telegram")


@router.get("")
def status(request: Request, user=Depends(current_user), db=Depends(get_db)):
    link = db.get(TelegramLink, user.id)
    return {"available": request.app.state.bot is not None, "linked": bool(link and link.chat_id)}


@router.post("/link")
def link(request: Request, user=Depends(current_user), db=Depends(get_db)):
    bot = request.app.state.bot
    if bot is None:
        raise HTTPException(503, "Telegram isn't set up on this laptop yet.")
    try:
        username = bot.username()
    except Exception:
        raise HTTPException(502, "Couldn't reach Telegram. Try again in a minute.") from None
    return {"url": f"https://t.me/{username}?start={new_link_token(db, user)}"}


@router.delete("")
def unlink(user=Depends(current_user), db=Depends(get_db)):
    link = db.get(TelegramLink, user.id)
    if link is not None:
        db.delete(link)
        db.commit()
    return {"linked": False}
