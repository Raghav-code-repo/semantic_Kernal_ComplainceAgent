# logging_conf.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

audit_logger = logging.getLogger("audit")