import logging
from functools import wraps

# Configure logging
logging.basicConfig(filename="actions.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_action(action):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logging.info(f"{action} executed")
            return func(*args, **kwargs)
        return wrapper
    return decorator
