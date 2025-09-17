import argparse
from dataclasses import dataclass


@dataclass
class FortunaConfig:
    api_base: str = "http://localhost:8000"
    api_key: str = ""
    log_level: str = "INFO"

    def __init__(self):
        parser = argparse.ArgumentParser(description="MCP Server Fortuna Flow")

        parser.add_argument(
            "--api_base",
            type=str,
            default="http://localhost:8000",
            help="Base URL for Fortuna API, default: http://localhost:8000",
        )
        parser.add_argument(
            "--api_key",
            type=str,
            required=True,
            help="API Key for Fortuna service",
        )
        parser.add_argument(
            "--log_level",
            type=str.upper,
            default="INFO",
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            help="Log level (case insensitive), default: INFO",
        )

        args = parser.parse_args()
        self.api_base = args.api_base
        self.api_key = args.api_key
        self.log_level = args.log_level.upper()
