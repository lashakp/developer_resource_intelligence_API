import json
import os
from collections import Counter, defaultdict
from statistics import mean

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ENRICHED_PATH = os.path.join(
    BASE_DIR, "..", "data", "enriched", "resources_enriched.json"
)

EVAL_DIR = os.path.join(BASE_DIR, "..", "data", "evaluation")
SUMMARY_PATH = os.path.join(EVAL_DIR, "evaluation_summary.json")


REQUIRED_FIELDS = {
    "resource_id",
    "resource_name",
    "source_url",
    "domain",
    "category",
    "resource_type",
    "skill_cluster",
    "domain_weight",
}


def load_enriched_data(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate_schema(resources):
    missing_field_counts = Counter()

    for r in resources:
        for field in REQUIRED_FIELDS:
            if field not in r or r[field] in (None, "", []):
                missing_field_counts[field] += 1

    return dict(missing_field_counts)


def distribution_stats(resources):
    skill_clusters = Counter()
    categories = Counter()
    domains = Counter()
    domain_weights = []

    for r in resources:
        skill_clusters[r["skill_cluster"]] += 1
        categories[r["category"]] += 1
        domains[r["domain"]] += 1
        domain_weights.append(r["domain_weight"])

    return {
        "skill_cluster_distribution": dict(skill_clusters),
        "top_categories": categories.most_common(15),
        "top_domains": domains.most_common(15),
        "avg_domain_weight": round(mean(domain_weights), 3),
        "max_domain_weight": max(domain_weights),
    }


def dominance_analysis(resources, threshold=0.1):
    """
    Detects domains contributing more than X% of total records.
    """
    domain_counts = Counter(r["domain"] for r in resources)
    total = len(resources)

    dominant = {
        d: round(c / total, 3)
        for d, c in domain_counts.items()
        if c / total >= threshold
    }

    return dominant


def evaluate(resources):
    return {
        "record_count": len(resources),
        "schema_issues": evaluate_schema(resources),
        "distribution": distribution_stats(resources),
        "dominant_domains": dominance_analysis(resources),
    }


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    os.makedirs(EVAL_DIR, exist_ok=True)

    print("Starting evaluation stage...")

    resources = load_enriched_data(ENRICHED_PATH)
    print(f"Loaded {len(resources)} enriched records")

    evaluation = evaluate(resources)

    save_json(evaluation, SUMMARY_PATH)

    print("Evaluation stage completed")
    print(f"Evaluation summary written to: {SUMMARY_PATH}")

    print("\nHigh-level signals:")
    print(f"- Total records: {evaluation['record_count']}")
    print(f"- Skill clusters: {list(evaluation['distribution']['skill_cluster_distribution'].keys())}")
    print(f"- Avg domain weight: {evaluation['distribution']['avg_domain_weight']}")
    print(f"- Dominant domains detected: {len(evaluation['dominant_domains'])}")


if __name__ == "__main__":
    main()
