import logging

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)


def produce_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(f"solution.{name}")
    logger.setLevel(logging.INFO)
    return logger


# Some additional logger logic ...
