import logging
import random
import time

# Get the logger name from the module name
# Module ame is 'base.base_node' -> logger name is 'base.base_node'
logger = logging.getLogger(__name__)


class FakeException(Exception):

    def __init__(self, message):
        message = f"{message} - This is a fake exception to simulate an error"
        super().__init__(message)

    def __str__(self):
        return f"FakeException: {self.args[0]}"


class ExtraLoggingAdapter(logging.LoggerAdapter):
    """Injects additional 'extra' fields into the log record"""

    def process(self, msg, kwargs):
        extra = self.extra.copy()
        if "extra" in kwargs:
            extra.update(kwargs["extra"])
        kwargs["extra"] = extra
        return msg, kwargs


class NodeLoggingAdapter(ExtraLoggingAdapter):
    """Injects node-class specific 'extra' fields into the log record"""

    def process(self, msg, kwargs):
        self.extra["node_id"] = self.extra.get("node_id", "N/A")
        self.extra["node_type"] = self.extra.get("node_type", "N/A")
        return super().process(msg, kwargs)


def _id_generator(prefix=""):
    yield f"{prefix}-{time.time_ns()}"


class BaseNode:

    _id_generator = _id_generator("node")

    def __init__(self, error_probability=0.1):
        self.id = next(self._id_generator)
        self.error_probability = error_probability
        # The adapted logger belongs to the class and is used for logging messages from the node class
        # Is is retrievable globally by calling >>> logging.getLogger(base.base_node)
        self.logger = self._build_logger()

    def _build_logger(self):
        return NodeLoggingAdapter(
            logger,
            {
                "node_id": self.id,
                "node_type": self.__class__.__name__,
            },
        )

    def run(self):
        self.logger.info("Running node")
        try:
            # Do something
            while True:
                time.sleep(0.5)
                self.logger.info("Node continues to run")
                # Roll dice to raise an exception
                if random.random() < self.error_probability:
                    # Simulate an error
                    raise FakeException("An error occurred")
        except FakeException as e:
            self.logger.exception(e)
            self.stop()

    def stop(self):
        self.logger.info("Stopping node")
