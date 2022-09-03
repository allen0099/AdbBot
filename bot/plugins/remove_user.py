import logging

from bot.user_management import get_allowed_users, remove_allowed_user
from pyrogram import Client, filters
from pyrogram.types import Message

from core.decorator import event_log
from core.log import main_logger

log: logging.Logger = main_logger(__name__)


@Client.on_message(filters.command("remove_user") & ~filters.forwarded)
@event_log
async def remove_user(_: Client, msg: Message) -> None:
    if len(msg.command) != 2:
        await msg.reply_text("Usage:\n" "<code>  /remove_user uid</code>")
        return

    if msg.from_user.id not in get_allowed_users():
        await msg.reply_text("You are not allowed to use this command.")
        return

    try:
        user_id: int = int(msg.command[1])
    except:
        await msg.reply_text("Uid field is not int only.")
        return

    if remove_allowed_user(user_id):
        await msg.reply_text(f"Removed {user_id} successfully.")
        return

    else:
        await msg.reply_text(f"User {user_id} are not in list.")
        return