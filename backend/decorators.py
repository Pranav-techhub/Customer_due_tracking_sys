import pandas as pd
from datetime import datetime
from functools import wraps
from pathlib import Path

# Path for logs.csv
DATA_PATH = Path(__file__).parent / "data"
LOGS_FILE = DATA_PATH / "logs.csv"

# Ensure logs.csv exists
if not LOGS_FILE.exists():
    pd.DataFrame(columns=["timestamp", "action", "status"]).to_csv(LOGS_FILE, index=False)

def log_action(action):
    """Decorator to log API actions into logs.csv"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                status = "success"
            except Exception as e:
                status = f"error: {e}"
                raise e
            finally:
                log_entry = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "action": action,
                    "status": status
                }
                df = pd.read_csv(LOGS_FILE)
                df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
                df.to_csv(LOGS_FILE, index=False)
            return result
        return wrapper
    return decorator
