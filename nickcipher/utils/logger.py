import logging
from pathlib import Path
from nickcipher.config import LOGS_DIR

LOG_FILE = LOGS_DIR / "nickcipher.log"
LOGS_DIR.mkdir(exist_ok=True)

def get_logger(name: str = "nickcipher"):
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger