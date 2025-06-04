# logging.py
import logging

__All__ = ["log"]

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
