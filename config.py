"""
CrowdWisdomTrading AI Agent
Main configuration and setup module
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
import sys

# Load environment variables
load_dotenv()

class Config:
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    DEFAULT_MODEL = "mistral/mistral-large-latest"
    FALLBACK_MODEL = "mistral/mistral-medium-latest"
    TEMPERATURE = 0.1
    MAX_TOKENS = 4000
    HEADLESS_BROWSER = os.getenv("HEADLESS_BROWSER", "true").lower() == "true"
    REQUEST_TIMEOUT = 30
    MAX_RETRIES = 3
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    TARGET_SITES = [
        {"name": "polymarket","base_url": "https://polymarket.com","markets_endpoint": "/markets"},
        {"name": "kalshi", "base_url": "https://kalshi.com","markets_endpoint": "/markets"},
        {"name": "prediction-market", "base_url": "https://www.prediction-market.com","markets_endpoint": "/markets"}
    ]
    OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "./output"))
    CSV_OUTPUT_PATH = Path(os.getenv("CSV_OUTPUT_PATH", "./output/unified_products.csv"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls):
        errors = []
        if not cls.MISTRAL_API_KEY:
            errors.append("MISTRAL_API_KEY is required")
        if not cls.OUTPUT_DIR.exists():
            cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        return True

def setup_logging():
    logger.remove()
    logger.add(
        sys.stderr,
        level=Config.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )
    log_file = Config.OUTPUT_DIR / "crowdwisdom_trading.log"
    logger.add(
        str(log_file),
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
        rotation="10 MB",
        retention="7 days"
    )
    return logger

setup_logging()
Config.validate()
logger.info("CrowdWisdomTrading AI Agent - Configuration loaded successfully")
