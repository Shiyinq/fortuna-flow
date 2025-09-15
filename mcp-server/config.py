import argparse
from dataclasses import dataclass


@dataclass
class FortunaConfig:
    api_base: str = "http://localhost:8000"
    api_key: str = ""

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

        args = parser.parse_args()
        self.api_base = args.api_base
        self.api_key = args.api_key
