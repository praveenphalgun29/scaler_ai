import json, os

POOL_FILE = "pools.json"

def load_pools():
    if not os.path.exists(POOL_FILE):
        raise Exception("Run build_pools.py once to generate pools.json")
    with open(POOL_FILE, "r", encoding="utf8") as f:
        return json.load(f)
