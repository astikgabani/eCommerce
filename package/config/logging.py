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
            "filename": constants.get_path(
                "log", "main.log", root_path=os.path.dirname(constants.ROOT_PATH)
            ),
        }
    },
    "root": {"level": "INFO", "handlers": ["wsgi"]},
}
