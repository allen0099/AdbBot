import logging
import re
from subprocess import Popen, PIPE, STDOUT, CalledProcessError
from urllib.parse import ParseResult, urlparse

from pyrogram import Client, filters
from pyrogram.types import Message

from bot.user_management import get_allowed_users
from core import settings
from core.decorator import event_log
from core.log import main_logger

log: logging.Logger = main_logger(__name__)
EXECUTE_FILE: str = "new_domain.sh"


@Client.on_message(filters.command("add") & ~filters.forwarded)
@event_log
async def add_domain(_: Client, msg: Message) -> None:
    if len(msg.command) != 2:
        await msg.reply_text("Usage:\n" "<code>  /add new_link</code>")
        return

    if msg.from_user.id not in get_allowed_users():
        await msg.reply_text("You are not allowed to use this command.")
        return

    new_domain: str = msg.command[1]

    if not check_validate_url(new_domain):
        await msg.reply_text("Invalid url.\n")
        return

    if not new_domain.startswith("http"):
        new_domain = "https://" + new_domain

    url: ParseResult = urlparse(new_domain)
    command: str = f"{settings.BASE_DIR}/{EXECUTE_FILE} {url.netloc}"

    # Execute command
    # https://stackoverflow.com/a/69480363
    process = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT)
    with process.stdout:
        try:
            for line in iter(process.stdout.readline, b""):
                log.debug(line.decode("utf-8").rstrip())

        except CalledProcessError as e:
            log.debug(f"{str(e)}")

    returned_value: int = process.returncode

    if returned_value != 0:
        await msg.reply_text("Cannot complete the operation.")
        return


def check_validate_url(url: str) -> bool:
    # https://github.com/django/django/blob/stable/4.1.x/django/core/validators.py#L79
    ul = "\u00a1-\uffff"  # Unicode letters range (must not be a raw string).
    # Host patterns
    hostname_re = (
        r"[a-z" + ul + r"0-9](?:[a-z" + ul + r"0-9-]{0,61}[a-z" + ul + r"0-9])?"
    )
    # Max length for domain name labels is 63 characters per RFC 1034 sec. 3.1
    domain_re = r"(?:\.(?!-)[a-z" + ul + r"0-9-]{1,63}(?<!-))*"
    tld_re = (
        r"\."  # dot
        r"(?!-)"  # can't start with a dash
        r"(?:[a-z" + ul + "-]{2,63}"  # domain label
        r"|xn--[a-z0-9]{1,59})"  # or punycode label
        r"(?<!-)"  # can't end with a dash
        r"\.?"  # may have a trailing dot
    )
    host_re = "(" + hostname_re + domain_re + tld_re + "|localhost)"

    regex = re.search(host_re, url, re.IGNORECASE)

    if regex:
        return True
    else:
        return False
