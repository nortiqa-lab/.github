"""Thin adapter for an existing Telegram polling/webhook app.

Example integration (pseudo):

    from nl.adapter import handle_telegram_text

    async def on_message(update):
        user_id = str(update.effective_user.id)
        chat_id = str(update.effective_chat.id)
        text = update.message.text or ""
        reply = handle_telegram_text(text, user_id=user_id, chat_id=chat_id)
        await update.message.reply_text(reply)

Do not import telegram token into this module.
"""

from __future__ import annotations

from typing import Optional

from nl.service import process_message


def handle_telegram_text(
    text: str,
    *,
    user_id: Optional[str] = None,
    chat_id: Optional[str] = None,
    live_health: bool = True,
) -> str:
    result = process_message(
        text,
        user_id=user_id,
        chat_id=chat_id,
        live_health=live_health,
        skip_auth=False,
    )
    return result.reply
