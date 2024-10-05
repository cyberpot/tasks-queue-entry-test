import logging

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)


def produce_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"solution.{name}")


# Some additional logger logic ...
