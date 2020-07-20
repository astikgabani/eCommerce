import os
from constants import constants

log_config = {
    "version": 1,
    "formatters": {
        "default": {"format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"}
    },
    "handlers": {
        "wsgi": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": os.path.join("log", "main.log")
        }
    },
    "root": {"level": "INFO", "handlers": ["wsgi"]},
}
