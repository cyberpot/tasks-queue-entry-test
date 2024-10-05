import logging


def produce_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"solution.{name}")


# Some additional logger logic ...
