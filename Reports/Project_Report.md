Developer Resource Intelligence API
1. Problem Definition

Developers face increasing difficulty identifying high-quality learning resources due to:

Information overload

Lack of intent awareness

No trust or authority signals

Opaque ranking algorithms

Search engines optimize for relevance, not learning quality or explainability.

2. Project Objective

To build a recommendation system that:

Enables structured discovery

Provides deterministic, explainable ranking

Supports ML ranking without risking reliability

Is production-ready and testable

Supports controlled public access (Demo mode)

3. Data Engineering & ETL
ETL Flow
Extract → Transform → Enrich → Load


Extract

Raw curated JSON sources

No schema assumptions

Transform

Schema normalization

Skill & resource type standardization

Enrich

Domain metadata

Deterministic domain_weight

GitHub detection

Summary statistics

Load

Seeded SQLite database

Deterministic, repeatable startup

4. Database Design

SQLite for portability

SQLAlchemy ORM

Read-only workload

Seeded once, consumed many times

5. API Architecture
Layered Separation
Layer	Responsibility
Routes	HTTP & validation
Service	Business orchestration
Ranking	ML vs deterministic enforcement
Scoring	Heuristic logic
Demo	Controlled public output
ML	Optional prediction
Schemas	Contract enforcement

This separation enabled:

Safer refactors

Isolated testing

Clear reasoning paths

6. Recommendation System Evolution
Initial State

Logic embedded in routes

Hard to test

Poor extensibility

Refactor Outcome

Thin routes

Testable services

Explicit ranking decisions

Demo vs Full access abstraction

This evolution was intentional architectural hardening, not churn.

7. Ranking System Design
Deterministic Ranking (Baseline)

Signals:

Domain authority

GitHub bonus

Resource type weighting

Properties:

Fully explainable

Stable

Always available

ML Ranking (Optional)

Lightweight linear model

Lazy-loaded

Automatically activated

Explicit fallback

Key Guarantee:
ML never silently fails. The API always reports the ranking source.

8. Demo vs Full Access Enforcement
Demo Mode

Deterministic only

Safe public exposure

No ML dependency

Shaped responses

Ideal for previews

Full Mode

Enables ML when available

Includes scores

Same API contract

Transparent ranking source

9. Testing Strategy

Unit tests for scoring

Integration tests for ranking mode switching

Contract tests for demo vs full parity

Result:

No brittle behavior

Predictable outputs

Safe ML extensibility

10. Deployment

Dockerized

Environment-agnostic

Swagger UI enabled

Simple startup

8. Deployment & Production Readiness

The application is containerized using Docker and deployed via Railway.

Deployment characteristics:
- Cloud-hosted containerized runtime
- Environment-based configuration (API keys, demo mode)
- Zero local setup required for reviewers
- Publicly accessible API endpoint

The deployed API exposes interactive documentation via Swagger UI, enabling real-time exploration of endpoints and ranking behavior.


11. Final Outcome

A production-grade backend demonstrating:

Data engineering

Clean API design

Explainable ranking

Safe ML integration

Defensive engineering practices