"""Allowlist auth for Telegram updates (no tokens here)."""

from __future__ import annotations

import os
from typing import Iterable, Optional, Set


def _parse_ids(raw: Optional[str]) -> Set[str]:
    if not raw:
        return set()
    return {part.strip() for part in raw.split(",") if part.strip()}


def allowed_user_ids() -> Set[str]:
    return _parse_ids(os.environ.get("TELEGRAM_ALLOWED_USER_IDS"))


def allowed_chat_ids() -> Set[str]:
    return _parse_ids(os.environ.get("TELEGRAM_ALLOWED_CHAT_IDS"))


def is_authorized(
    user_id: Optional[str] = None,
    chat_id: Optional[str] = None,
    *,
    users: Optional[Iterable[str]] = None,
    chats: Optional[Iterable[str]] = None,
    fail_closed: bool = True,
) -> bool:
    """Authorize if user or chat is allowlisted.

    If both allowlists are empty and fail_closed=True → deny (safe default).
    """
    u_set = set(users) if users is not None else allowed_user_ids()
    c_set = set(chats) if chats is not None else allowed_chat_ids()

    if not u_set and not c_set:
        return not fail_closed

    uid = str(user_id) if user_id is not None else None
    cid = str(chat_id) if chat_id is not None else None
    if uid and uid in u_set:
        return True
    if cid and cid in c_set:
        return True
    return False
