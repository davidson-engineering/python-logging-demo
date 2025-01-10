LOGGING_CONFIG = {
    "version": 1,  # You must include this or the config doesn't work. It's to ensure backward compatibility
    "disable_existing_loggers": True,  # Disable any existing loggers that are already configured
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        "node": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: {%(node_id)s} %(message)s"
        },
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "fmt": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "console_node": {
            "level": "INFO",
            "formatter": "node",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "base_file": {
            "level": "DEBUG",
            "formatter": "json",
            "class": "logging.FileHandler",
            "filename": "base_debug.log",
            "mode": "w",
        },
        "custom_file": {
            "level": "DEBUG",
            "formatter": "json",
            "class": "logging.FileHandler",
            "filename": "custom_debug.log",
            "mode": "w",
        },
    },
    "loggers": {
        # root logger. This ensures that all unaccounted log messages are written to the console
        "": {
            "handlers": ["default"],
            "level": "WARNING",
            "propagate": False,
        },
        # Logger for the 'base' module
        # Logs from this logger will be written to the console and to a file
        # Note that the custom node handler is used to ensure that the node_id is included in the log message sent to console output
        "base": {
            "handlers": ["console_node", "base_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        # Logger for the 'custom' module
        # Logs from this logger will be written to the console and to a file
        # Note that the custom node handler is used to ensure that the node_id is included in the log message sent to console output
        "custom": {
            "handlers": ["console_node", "custom_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        # Logger for the '__main__' module
        # Note that the default handler is used to log messages from the main module
        "__main__": {  # if __name__ == '__main__'
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
