import random
import string
import logging

from ..base.base_node import BaseNode

logger = logging.getLogger(__name__)


class BackwardsLoggerAdapter(logging.LoggerAdapter):

    whitelist = ["info"]

    # This adapter reverses all fields (because this definitely a real-world use case)
    # It also adds a custom field 'backwards' to the log message
    def process(self, msg, kwargs):
        # reverse msg
        try:
            msg = msg[::-1]
            msg = msg + f"- [backwards={self.extra['backwards']}]"
        except TypeError:
            pass
        return super().process(msg, kwargs)


def _id_generator(prefix=""):
    while True:
        # Generate alphabetical 10-char node IDs
        yield f"{prefix}-{''.join(random.choices(string.ascii_lowercase, k=10))}"


class BackwardsNode(BaseNode):

    _id_generator = _id_generator("backwards")

    def _build_logger(self):
        return BackwardsLoggerAdapter(
            logger,
            {
                "node_id": self.id,
                "node_type": self.__class__.__name__,
                "backwards": True,
            },
        )
