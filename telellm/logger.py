import logging
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        level = logger.level(record.levelname).name
        logger.log(level, record.getMessage())


def init_logger():
    logging.getLogger("aiogram").setLevel(logging.DEBUG)
    logging.getLogger("aiogram").addHandler(InterceptHandler())
    logging.getLogger("asyncio").setLevel(logging.DEBUG)
    logging.getLogger("asyncio").addHandler(InterceptHandler())
