import json
import os

# Resolve project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENRICHED_PATH = os.path.join(
    BASE_DIR,
    "data",
    "enriched",
    "resources_enriched.json"
)

# Load enriched resources once at startup
with open(ENRICHED_PATH, "r", encoding="utf-8") as f:
    RESOURCES = json.load(f)
