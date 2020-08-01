import os
from constants import constants

log_root_dir = "log"

if not os.path.exists(log_root_dir):
    os.mkdir(log_root_dir)

log_config = {
    "version": 1,
    "formatters": {
        "default": {"format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"}
    },
    "handlers": {
        "wsgi": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": os.path.join(log_root_dir, "main.log"),
        }
    },
    "root": {"level": "INFO", "handlers": ["wsgi"]},
}
