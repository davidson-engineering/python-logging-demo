import logging

# Refer to these links for the escape codes:
# https://en.wikipedia.org/wiki/ANSI_escape_code
# https://gist.github.com/ConnerWill/d4b6c776b509add763e17f9f113fd25b


# Various Json Formatters
# *************************************************************
# Link: https://stackoverflow.com/questions/50144628/python-logging-into-file-as-a-dictionary-or-json

# python-json-logger
from pythonjsonlogger.json import JsonFormatter


class JsonFormatter(JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record["levelname"] = record.levelname
        log_record["module"] = record.module
        log_record["lineno"] = record.lineno
        log_record["message"] = record.getMessage()
        log_record["asctime"] = self.formatTime(record, self.datefmt)


# No dependencies required, but some limitations
import json


# This formatter will dump all log record attributes into JSON
class VerboseJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        super().format(record)
        output = {k: str(v) for k, v in record.__dict__.items()}
        return json.dumps(output)


# This formatter will dump only the log level, date, message, module, and line number into JSON
class SelectiveJsonFormatter(logging.Formatter):
    """Formatter to dump error message into JSON"""

    def format(self, record: logging.LogRecord) -> str:
        record_dict = {
            "level": record.levelname,
            "date": self.formatTime(record),
            "message": record.getMessage(),
            "module": record.module,
            "lineno": record.lineno,
        }
        return json.dumps(record_dict)


# Various Colored Formatters
# *************************************************************


class ColoredLogLevelFormatter(logging.Formatter):
    # Define ANSI color codes
    COLORS = {
        "DEBUG": "\033[94m",  # Blue
        "INFO": "\033[92m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[95m",  # Magenta
        "RESET": "\033[0m",  # Reset color
    }

    def format(self, record):

        # Apply color to the log level
        color = self.COLORS.get(record.levelname, "")
        reset = self.COLORS["RESET"]
        record.levelname = f"{color}{record.levelname:<5}{reset}"

        return super().format(record)


def split_name(name):
    """Split a logger name into its components, return last component"""
    return name.split(".")[-1]


class ColoredNodeFormatter(ColoredLogLevelFormatter):

    def format(self, record):
        """Colorize log entry"""
        # Bold bright white on blue background for the logger name
        # Only display the last part of the logger name
        record.name = f"\033[97;44m{split_name(record.name)}\033[0m"
        # Set node_id as bold
        record.node_id = f"\033[1m{record.node_id}\033[22m"
        # Set node_type as italic
        record.node_type = f"\033[3m{record.node_type}\033[23m"
        # Color log message in yellow
        # By using the record.message (instead of 'msg') attribute, we can ignore any formatting applied by the base class
        record.msg = f"\033[38;5;226m{record.message}\033[0m"
        # Color the log message in red and bold it if error
        if record.levelname == "ERROR":
            record.msg = f"\033[1;31m{record.message}\033[0m"
        return super().format(record)


class SubmoduleLogFormatter(ColoredLogLevelFormatter):

    def format(self, record):
        """Colorize entire log messages, set to green for warnings, yellow for info, and red for errors"""
        if record.levelno == logging.WARNING:
            record.msg = f"\033[92m{record.message}\033[0m"
        if record.levelno == logging.INFO:
            record.msg = f"\033[93m{record.message}\033[0m"
        if record.levelno == logging.ERROR:
            record.msg = f"\033[91m{record.message}\033[0m"
        return super().format(record)
