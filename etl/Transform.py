import json
import os
import re
import hashlib
from datetime import datetime, timezone
from urllib.parse import urlparse
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_PATH = os.path.join(BASE_DIR, "..", "data", "raw", "resources_raw.json")
PROCESSED_DIR = os.path.join(BASE_DIR, "..", "data", "processed")
CLEAN_JSON_PATH = os.path.join(PROCESSED_DIR, "resources_clean.json")
CLEAN_CSV_PATH = os.path.join(PROCESSED_DIR, "resources_clean.csv")


def load_raw_data(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def clean_text(text):
    if not text:
        return None
    text = text.strip()
    text = re.sub(r"[^\w\s\-]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def normalize_category(category):
    """
    Normalize category text and prevent token duplication.
    This permanently prevents cases like:
    - databasedatabase
    - database database
    - database+database
    """
    if not category:
        return "uncategorized"

    category = category.lower()

    # Remove non-letter characters
    category = re.sub(r"[^a-z\s]", " ", category)

    # Tokenize
    tokens = category.split()
    if not tokens:
        return "uncategorized"

    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for token in tokens:
        if token not in seen:
            seen.add(token)
            deduped.append(token)

    return " ".join(deduped)


def extract_domain(url):
    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return None


def infer_resource_type(name, domain):
    name = (name or "").lower()
    domain = (domain or "").lower()

    if "github.com" in domain:
        return "repository"
    if any(k in name for k in ["docs", "documentation"]):
        return "documentation"
    if any(k in name for k in ["course", "tutorial", "learn"]):
        return "course"
    if "medium.com" in domain or "blog" in name:
        return "article"
    return "tool"


def generate_resource_id(url):
    return hashlib.md5(url.encode("utf-8")).hexdigest()


def transform_resources(raw_resources):
    seen_urls = set()
    cleaned = []

    for r in raw_resources:
        url = r.get("source_url")
        if not url or url in seen_urls:
            continue

        seen_urls.add(url)

        name = clean_text(r.get("resource_name"))
        category = normalize_category(r.get("category"))
        domain = extract_domain(url)
        resource_type = infer_resource_type(name, domain)

        cleaned.append({
            "resource_id": generate_resource_id(url),
            "resource_name": name,
            "source_url": url,
            "domain": domain,
            "category": category,
            "resource_type": resource_type,
            "is_github": domain == "github.com",
            "extracted_at": r.get("extracted_at"),
            "transformed_at": datetime.now(timezone.utc).isoformat()
        })

    return cleaned


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_csv(data, path):
    if not data:
        return

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    print("Starting transform stage...")

    raw = load_raw_data(RAW_PATH)
    print(f"Loaded {len(raw)} raw records")

    cleaned = transform_resources(raw)
    print(f"Transformed into {len(cleaned)} clean records")

    save_json(cleaned, CLEAN_JSON_PATH)
    save_csv(cleaned, CLEAN_CSV_PATH)

    print("Transform stage completed successfully")
    print(f"JSON output: {CLEAN_JSON_PATH}")
    print(f"CSV output: {CLEAN_CSV_PATH}")


if __name__ == "__main__":
    main()
