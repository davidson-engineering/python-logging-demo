import random
import string
import logging

from base.base_node import BaseNode, NodeLoggingAdapter

logger = logging.getLogger(__name__)


class BackwardsLoggerAdapter(NodeLoggingAdapter):
    # This adapter reverses all fields (because this definitely a real-world use case)
    def process(self, msg, kwargs):
        # reverse all fields
        extra = self.extra.copy()
        for key in extra:
            try:
                extra[key] = extra[key][::-1]
            except TypeError:
                # If the field is not a string, just continue
                pass
        if "extra" in kwargs:
            extra.update(kwargs["extra"])


def _id_generator(prefix=""):
    # Generate 10 digit alphanumeric node IDs, because this node likes to be different
    id_ = "".join(random.choices(string.ascii_letters + string.digits, k=10))
    yield f"{prefix}-{id_}"


class BackwardsNode(BaseNode):
    _id_generator = _id_generator("backwards_node")

    def _build_logger(self):
        return BackwardsLoggerAdapter(
            logger,
            {
                "node_id": self.id,
                "node_type": self.__class__.__name__,
                "backwards": True,
            },
        )
