import json
import os
from datetime import datetime

HISTORY_FILE = "database/query_history.json"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)
    
def save_query(query, status):
    history = load_history()

    entry = {
        "query": query,
        "status": status,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    history.insert(0, entry)
    history = history[:10]

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)