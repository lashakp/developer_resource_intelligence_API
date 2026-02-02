import json
import os
from collections import Counter
from datetime import datetime, timezone
import re

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_PATH = os.path.join(BASE_DIR, "..", "data", "processed", "resources_clean.json")
ENRICHED_DIR = os.path.join(BASE_DIR, "..", "data", "enriched")

ENRICHED_DATA_PATH = os.path.join(ENRICHED_DIR, "resources_enriched.json")
CATEGORY_SUMMARY_PATH = os.path.join(ENRICHED_DIR, "category_summary.json")
DOMAIN_SUMMARY_PATH = os.path.join(ENRICHED_DIR, "domain_summary.json")

# -----------------------------
# Skill keyword mapping
# -----------------------------
SKILL_KEYWORDS = {
    "frontend": ["javascript", "css", "react", "vue", "frontend", "accessibility"],
    "backend": ["backend", "api", "server", "node", "django", "flask"],
    "data": ["data", "database", "sql", "pandas", "numpy", "machine learning", "ml", "analytics"],
    "devops": ["docker", "kubernetes", "devops", "ci", "cd"],
    "mobile": ["android", "ios", "flutter", "react native"],
}

# -----------------------------
# Load clean data
# -----------------------------
def load_clean_data(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# -----------------------------
# Category normalization (FIXED)
# -----------------------------
def normalize_category(category):
    if not category:
        return "unknown"

    text = category.lower()

    # Remove collapsed anchor artifacts
    text = re.sub(r"^a\s*name", "", text)
    text = re.sub(r"a$", "", text)

    # Remove non-letters
    text = re.sub(r"[^a-z]", "", text)

    if not text:
        return "unknown"

    # ---- FIX duplicated concatenations ----
    # databasedatabase -> database
    half = len(text) // 2
    if len(text) % 2 == 0 and text[:half] == text[half:]:
        text = text[:half]

    return text


# -----------------------------
# Skill clustering (FIXED)
# -----------------------------
def assign_skill_cluster(resource):
    text = f"{resource.get('resource_name', '')} {resource.get('category', '')}".lower()

    for cluster, keywords in SKILL_KEYWORDS.items():
        if any(k in text for k in keywords):
            return cluster
    return "general"

# -----------------------------
# Summaries
# -----------------------------
def build_summaries(resources):
    category_counter = Counter()
    domain_counter = Counter()

    for r in resources:
        category_counter[r.get("category", "unknown")] += 1
        domain_counter[r.get("domain", "unknown")] += 1

    return category_counter, domain_counter

# -----------------------------
# Enrichment
# -----------------------------
def enrich_resources(resources, domain_counts):
    enriched = []

    for r in resources:
        normalized_category = normalize_category(r.get("category"))

        enriched.append({
            **r,
            "category": normalized_category,
            "category_slug": normalized_category.replace(" ", "_"),
            "skill_cluster": assign_skill_cluster({
                **r,
                "category": normalized_category
            }),
            "domain_weight": domain_counts.get(r.get("domain"), 0),
            "enriched_at": datetime.now(timezone.utc).isoformat()
        })

    return enriched

# -----------------------------
# Save JSON
# -----------------------------
def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# -----------------------------
# Main
# -----------------------------
def main():
    os.makedirs(ENRICHED_DIR, exist_ok=True)

    print("Starting enrichment stage...")

    resources = load_clean_data(INPUT_PATH)
    print(f"Loaded {len(resources)} clean records")

    category_counts, domain_counts = build_summaries(resources)

    enriched_resources = enrich_resources(resources, domain_counts)

    save_json(enriched_resources, ENRICHED_DATA_PATH)
    save_json(dict(category_counts), CATEGORY_SUMMARY_PATH)
    save_json(dict(domain_counts), DOMAIN_SUMMARY_PATH)

    print("Enrichment stage completed successfully")
    print(f"Enriched data written to: {ENRICHED_DATA_PATH}")

    print("\nSample enriched record:")
    print(json.dumps(enriched_resources[0], indent=2))

if __name__ == "__main__":
    main()
