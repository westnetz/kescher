import logging


def setup_logging(cwd):
    """
    Creates and returnes a logger with the default logging level "INFO"
    in the current working directory.
    """
    logger = logging.getLogger("kescher")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(cwd / "kescher.log")
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
