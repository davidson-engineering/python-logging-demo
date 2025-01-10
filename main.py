from pathlib import Path
import sys
import time
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)


def load_yaml(filepath):

    import yaml

    with open(filepath, "r") as file:
        return yaml.safe_load(file)


def setup_logging(config: Dict[str, Any]):
    import logging.config

    logging.config.dictConfig(config)


if __name__ == "__main__":
    config = load_yaml(Path("logging_config.yaml"))
    setup_logging(config)

    from src.base.base_node import BaseNode
    from src.custom.custom_node import BackwardsNode

    try:
        nodes = []
        logger.info("Starting nodes")
        base_node_0 = BaseNode(error_probability=0.1)
        nodes.append(base_node_0)
        backwards_node_1 = BackwardsNode()
        nodes.append(backwards_node_1)

        for node in nodes:
            node.run()

        while True:
            # Hang around here while the nodes do stuff
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Shutting down nodes")
        sys.exit(0)
