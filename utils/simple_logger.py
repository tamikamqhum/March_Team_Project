import logging
import os
import sys
import functools
import streamlit as st
from functools import wraps

# Allow dynamic control of log level via environment variable or a default
# to change via terminal: export LOG_LEVEL=DEBUG (linux),
# set LOG_LEVEL=DEBUG (Windows)
# or alter in config.py
# Use DEBUG for detailed logs
# Can be DEBUG, INFO, WARNING, ERROR, CRITICAL


# Allow dynamic control of log level via environment variable or config file
# LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()
LOG_LEVEL = os.getenv("LOG_LEVEL", "ERROR").upper()
# Ensure logs directory exists

os.makedirs("sl_logs", exist_ok=True)

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def log_function_call(logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Calling: {func.__name__}")
            result = func(*args, **kwargs)
            logger.info(f"Completed: {func.__name__}")
            return result
        return wrapper
    return decorator