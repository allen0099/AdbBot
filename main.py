import logging

from bot import Bot
from core.log import (
    main_logger,
    PyrogramLogger,
)

log: logging.Logger = main_logger(__name__)
pg_log: logging.Logger = PyrogramLogger().logger

if __name__ == "__main__":
    bot: Bot = Bot()
    bot.run()

    log.info("Bye!")
    logging.shutdown()
