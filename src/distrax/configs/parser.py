import argparse
import configparser
import logging
from typing import Any, Dict, List


def set_logging(log_level: str = "info") -> int:
    """Set logging Level."""
    log = 20
    if log_level == "info":
        log = logging.INFO
    elif log_level == "debug":
        log = logging.DEBUG
    return log


def _argument_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=r"""
     /$$$$$$$  /$$$$$$  /$$$$$$  /$$$$$$$$ /$$$$$$$   /$$$$$$  /$$   /$$
    | $$__  $$|_  $$_/ /$$__  $$|__  $$__/| $$__  $$ /$$__  $$| $$  / $$
    | $$  \ $$  | $$  | $$  \__/   | $$   | $$  \ $$| $$  \ $$|  $$/ $$/
    | $$  | $$  | $$  |  $$$$$$    | $$   | $$$$$$$/| $$$$$$$$ \  $$$$/
    | $$  | $$  | $$   \____  $$   | $$   | $$__  $$| $$__  $$  >$$  $$
    | $$  | $$  | $$   /$$  \ $$   | $$   | $$  \ $$| $$  | $$ /$$/\  $$
    | $$$$$$$/ /$$$$$$|  $$$$$$/   | $$   | $$  | $$| $$  | $$| $$  \ $$
    |_______/ |______/ \______/    |__/   |__/  |__/|__/  |__/|__/  |__/
    """,
    )
    parser.add_argument(
        "-c",
        "--config-file",
        type=str,
        help="Config File holding setup information",
        required=True,
    )
    parser.add_argument(
        "-a",
        "--action",
        choices=["create", "remove"],
        help="Create or Remove DisTRaX Storage System",
        required=True,
    )
    parser.add_argument(
        "-log",
        "--log-level",
        choices=["info", "debug"],
        default="info",
        help="Logging Level",
        required=False,
    )
    return parser.parse_args()


def _read_config_file(
    config: Dict[str, Any], header: str, config_keys: List[str]
) -> Dict[Any, Any]:
    error = False
    if config.get(header) is not None:
        header_config = {k.lower(): v for k, v in config[header].items()}
        for key in config_keys:
            if header_config.get(key) is None:
                logging.error(f"{key} is missing from setup in config")
                error = True
            if header_config.get(key) == "":
                logging.error(f"{key} is missing a value from {header}")
                error = True
    else:
        logging.error(f"{header} is missing from config file")
        error = True
    if error:
        return dict()
    return header_config


def _config_parser(config_file: str) -> Dict[str, Any]:
    configs = {}
    config = configparser.ConfigParser()
    config.read(config_file)
    # convert keys to lowercase
    config_dict = {k.lower(): v for k, v in config.items()}
    setup_config_keys = ["backend", "folder", "interface", "number_of_hosts", "service"]
    setup_config_dict = _read_config_file(config_dict, "setup", setup_config_keys)

    if set(setup_config_dict.keys()).difference(setup_config_keys) == set():
        configs["backend"] = setup_config_dict["backend"]
        configs["folder"] = setup_config_dict["folder"]
        configs["interface"] = setup_config_dict["interface"]
        configs["number_of_hosts"] = int(setup_config_dict["number_of_hosts"])
        configs["service"] = setup_config_dict["service"]
        if setup_config_dict.get("log_level") is not None:
            configs["log_level"] = setup_config_dict.get("log_level")
    else:
        print(setup_config_dict.keys())
        logging.error("SETUP ERROR")
        return {}
    ram_config_keys = ["type", "number", "size_in_gb"]
    ram_config = _read_config_file(config_dict, "ram", ram_config_keys)
    if set(ram_config.keys()).difference(ram_config_keys) == set():
        configs["ram_type"] = ram_config["type"]
        configs["ram_number"] = int(ram_config["number"])
        configs["ram_size"] = int(ram_config["size_in_gb"])
    else:
        return {}

    return configs
