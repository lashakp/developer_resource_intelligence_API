Project Report
Developer Resource Intelligence API

1. Problem Definition

Modern developers face information overload when searching for learning resources. While search engines excel at keyword retrieval, they fail to optimize for:

Skill relevance (e.g., data vs backend vs devops)

Learning intent (tool vs documentation vs course)

Trustworthiness and source authority

Explainability of why a resource is recommended

This results in wasted time, inconsistent quality, and opaque ranking logic.

Project Objective

This project aims to build a transparent, explainable, and extensible recommendation system that:

Enables structured discovery of developer resources

Provides deterministic, explainable ranking

Supports optional ML-based ranking without sacrificing reliability

Is production-ready, testable, and deployable via Docker

2. Data Collection & ETL Pipeline
2.1 Data Sources

Raw resource data was collected from curated developer learning sources, including tools, documentation, articles, and courses. The emphasis was on quality over quantity to ensure meaningful ranking.

2.2 ETL Architecture

The project follows a logical ETL flow, implemented across multiple modules:

Extract → Transform → Enrich → Load

Extract

Raw JSON data ingested from source files

No assumptions made about schema consistency

Transform

Schema normalization

Field standardization (skill clusters, resource types)

Removal of malformed or incomplete entries

Enrich

Domain-level metadata added

Heuristic domain_weight introduced as an authority signal

GitHub detection flags (is_github)

Category and summary statistics generated

Load

Final enriched dataset persisted into SQLite via a database seed script

Load is intentionally handled outside the ETL folder to support:

Deterministic startup

Reproducibility

Deployment simplicity

Design decision: A standalone Load.py module was intentionally not required, as database seeding (db/seed.py) serves as the authoritative load mechanism.

Challenges Encountered

Inconsistent source formats

Missing metadata fields

Solutions Applied

Strict normalization rules

Defensive enrichment logic

Explicit schema validation downstream via Pydantic

3. Database Design
Technology Choice

SQLite selected for:

Portability

Zero-configuration deployment

Suitability for read-heavy workloads

ORM Layer

SQLAlchemy used for schema definition and database access

Models defined once and reused across seed and application layers

Data Lifecycle

Database is seeded once

API operates in read-only mode

Ensures predictable behavior across environments

4. API Architecture & Design
4.1 Versioning Strategy

All endpoints are versioned under /v1, enabling:

Backward compatibility

Future iteration without breaking clients

4.2 Separation of Concerns

The API was intentionally decomposed into clear architectural layers:

Layer	Responsibility
main.py	App configuration, lifecycle, router registration
routes/	HTTP interface, validation, documentation
service/	Business logic and orchestration
scoring.py	Deterministic scoring rules
ranking.py	ML vs fallback enforcement
ml/	Model loading and prediction
schemas.py	Contract enforcement

This separation made the system:

Easier to test

Easier to reason about

Safer to extend

5. Evolution of Recommendations Architecture
Initial State

Early iterations had recommendation logic mixed directly inside route handlers, leading to:

Tight coupling

Difficult testing

Poor clarity

Refactor Milestone

The system was refactored into:

recommendations.py → HTTP concerns only

service.py → business orchestration

ranking.py → ranking mode decision logic

scoring.py → deterministic scoring rules

Why This Matters

Routes remain thin and declarative

Service layer becomes testable in isolation

Ranking logic can evolve independently

This back-and-forth refinement was a deliberate architectural hardening process, not accidental churn.

6. Ranking System Design
6.1 Deterministic Scoring (Baseline)

Each resource is scored using transparent heuristics:

Domain authority (domain_weight)

GitHub bonus

Resource type weighting

Key properties:

Fully explainable

Debuggable

Stable

Deterministic

This ensures the API always works, even without ML.

6.2 ML Ranking Layer (Optional)

A lightweight linear ranking model is supported:

Loaded lazily at runtime

Automatically activated if present

Disabled gracefully if missing

Enforcement Logic

The ranking flow guarantees:

ML model is checked for availability

If present → ML predictions are used

If absent → deterministic scoring is enforced

API response explicitly reports ranking_mode

This avoids a common anti-pattern where ML silently fails.

7. Testing Strategy
Unit Tests

Scoring correctness

Ranking consistency

Integration Tests

Verified ML ranking activation

Verified deterministic fallback

Ensured identical API contract regardless of ranking mode

Outcome

No brittle behavior

No hidden dependency on model presence

Predictable system behavior

8. Deployment & Production Readiness
Dockerization

Single Docker image

Uvicorn + FastAPI

Environment-agnostic startup

docker build -t dev-resource-api .
docker run -p 8000:8000 dev-resource-api

API Documentation

Swagger UI auto-generated

Rich descriptions and examples

Help endpoint for human-readable guidance

9. Key Lessons Learned

Fallback systems are not optional
ML should enhance systems, not destabilize them.

Clear service boundaries reduce complexity
Testing and refactoring became easier after separation.

Explainability matters
Deterministic logic provides trust and debuggability.

Architecture evolves through iteration
Refactoring is a sign of maturity, not failure.

10. Final Outcome

The final system is a portfolio-grade backend demonstrating:

Data engineering (ETL + enrichment)

API design and versioning

Deterministic + ML ranking systems

Defensive engineering practices

Automated testing

Production deployment readiness

This project is suitable for:

GitHub showcasing

Technical interviews

Extension into personalization or SaaS products

11. Future Enhancements

API authentication

User-specific personalization

Caching layer (Redis)

Advanced ML models

Analytics endpoints

 Conclusion
 
The Developer Resource Intelligence API successfully bridges data engineering, backend architecture, and applied ML into a cohesive, reliable system. Its emphasis on explainability, fallback safety, and clean boundaries reflects real-world production engineering practices.