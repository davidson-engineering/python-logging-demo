import logging
import random
from threading import Thread
import time

# Get the logger name from the module name
# Module name is 'base.base_node' -> logger name is 'base.base_node'
logger = logging.getLogger(__name__)


class FakeException(Exception):

    def __init__(self, message):
        message = f"{message} - This is a fake exception to simulate an error"
        super().__init__(message)

    def __str__(self):
        return f"FakeException: {self.args[0]}"


def _id_generator(prefix=""):
    while True:
        # Generate pseudo-unique node IDs using the current time
        yield f"{prefix}-{str(time.time_ns())[:-10]}"


class BaseNode(Thread):

    _id_generator = _id_generator("node")

    def __init__(self, error_probability=0.1):
        super().__init__()
        self.id = next(self._id_generator)
        self.error_probability = error_probability
        # The adapted logger belongs to the class and is used for logging messages from the node class
        # Is is retrievable globally by calling >>> logging.getLogger(base.base_node)
        self.logger = self._build_logger()
        self._node_stopped = False

    def _build_logger(self):
        return logging.LoggerAdapter(
            logger,
            {
                "node_id": self.id,
                "node_type": self.__class__.__name__,
            },
        )

    def run(self):
        self.logger.info("Running node")
        try:
            while not self._node_stopped:
                time.sleep(0.5)
                self.logger.info("Node continues to run")
                if random.random() < self.error_probability:
                    raise FakeException("An error occurred")
        except FakeException as e:
            self.logger.error(e)
            self.stop()

    def stop(self):
        self.logger.info("Stopping node")
        self._node_stopped = True
