import logging
import sys


def configure_logging(level: str = "INFO", service_name: str = "scraper-api") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format=f"%(asctime)s [{service_name}] %(levelname)s %(name)s: %(message)s",
        stream=sys.stdout,
    )
