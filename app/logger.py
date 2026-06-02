import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(
            "store_intelligence.log"
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(
    "store_intelligence"
)