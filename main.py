from pathlib import Path
import random
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

    # Flush logs/master_log_file.log
    with open("logs/master_log_file.log", "w") as f:
        f.write("")

    config = load_yaml(Path("logging_config.yaml"))
    setup_logging(config)

    # Import a function from this submodule just to generate some logs from it.
    from node.base.submodule import ColoredNode

    # Note that the logger name is 'base.submodule' because the submodule is imported from 'base'
    submodule_node = ColoredNode()
    print("")
    print("submodule_node_logger_name:", submodule_node.logger.name)
    submodule_node.do_submodule_things()

    # Note that the logs are colored according to the format specified in base.logging_formats.SubmoduleLogFormatter
    # However, these logs are also written to the master log file, and do not have any color formatting applied
    # This is all configured in the logging_config.yaml file, and performed at the top level of the application

    # Let's make some more nodes and run them
    # Notice that the two node types have different node-id formats and different log message formats
    # These are defined using adapters in the node classes
    # There are no escape sequences in the log messages, so the logs will not be colored
    # The colors are only applied at the top level of the application

    # Base nodes get logged to a logs/base.log file
    # Custom nodes get logged to a logs/custom.log file
    # All log output is collected in the master log file

    # The formatting for the logs is defined in the base.logging_formats module
    # Note is completely untangled from the logs themselves
    # This means that the log formatting can be changed without changing the log messages
    # this approach is important for ensuring that the application can be easily maintained, tested and imported into other projects

    from node.base.base_node import BaseNode
    from node.custom.custom_node import BackwardsNode

    try:
        nodes = []
        logger.info("Starting nodes")
        base_nodes = [
            BaseNode(error_probability=random.uniform(0.1, 0.3)) for _ in range(5)
        ]
        nodes.extend(base_nodes)
        custom_nodes = [
            BackwardsNode(error_probability=random.uniform(0.1, 0.3)) for _ in range(5)
        ]
        nodes.extend(custom_nodes)

        # The nodes run in sequence
        for node in nodes:
            node.start()

        while True:
            # If all nodes have stopped, exit the loop
            if all(node._node_stopped for node in nodes):
                logger.info("All nodes stopped")
                break
            # Else hang around here while the nodes do stuff
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Shutting down nodes")
        sys.exit(0)
