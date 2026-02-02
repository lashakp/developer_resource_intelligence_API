import requests
import re
import json
import os
from datetime import datetime, timezone


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_PATH = os.path.join(BASE_DIR, "..", "data", "raw", "resources_raw.json")

GITHUB_RAW_URL = (
    "https://raw.githubusercontent.com/marcelscruz/dev-resources/master/README.md"
)


def fetch_markdown(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

def parse_resources(markdown_text):
    resources = []
    current_category = "Uncategorized"

    for line in markdown_text.split("\n"):
        # Capture headings of any level
        heading_match = re.match(r"#{1,6}\s+(.*)", line)
        if heading_match:
            current_category = heading_match.group(1).strip()
            continue

        # Capture markdown links
        links = re.findall(r"\[(.*?)\]\((https?://[^)]+)\)", line)
        for name, url in links:
            resources.append({
                "resource_name": name.strip(),
                "source_url": url.strip(),
                "category": current_category,
                "extracted_at": datetime.now(timezone.utc).isoformat()

            })

    return resources

def inspect_structure(markdown_text, n=50):
    lines = markdown_text.split("\n")
    print("\n--- SAMPLE README STRUCTURE ---")
    for line in lines[:n]:
        print(line)
    print("--- END SAMPLE ---\n")


def main():
    raw_dir = os.path.dirname(RAW_DATA_PATH)

    if os.path.exists(raw_dir) and not os.path.isdir(raw_dir):
        raise RuntimeError(f"{raw_dir} exists but is not a directory")

    os.makedirs(raw_dir, exist_ok=True)

    print("Starting extraction...")
    markdown = fetch_markdown(GITHUB_RAW_URL)
    print(f"Downloaded markdown length: {len(markdown)} characters")

    resources = parse_resources(markdown)
    print(f"Parsed {len(resources)} resources")

    with open(RAW_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(resources, f, indent=2, ensure_ascii=False)

    print(f"Raw data written to: {RAW_DATA_PATH}")
    
if __name__ == "__main__":
    main()