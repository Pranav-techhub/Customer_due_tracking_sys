import pandas as pd

def read_customers(file_path):
    if not file_path.exists():
        return []
    return pd.read_csv(file_path).to_dict(orient="records")

def write_customers(file_path, data):
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)

def assign_new_id(df: pd.DataFrame) -> int:
    """Find the smallest available ID starting from 1."""
    if df.empty:
        return 1
    existing_ids = sorted(df["id"].astype(int).tolist())
    for i in range(1, len(existing_ids) + 2):
        if i not in existing_ids:
            return i
