Developer Resource Intelligence API

## Live Deployment

The API is deployed and publicly accessible using Railway.

 **Live API (Swagger UI):**  
https://developerresourceintelligenceapi-production.up.railway.app/docs#/

The deployed instance supports:
- Demo mode (no API key required)
- Full mode with authenticated access


Overview

Developer Resource Intelligence API is a production-ready, explainable recommendation backend for curated developer learning resources.

It combines:

Deterministic, transparent ranking (always available)

Optional ML-based ranking (safely enabled when present)

Explicit Demo vs Full access modes

Clean, testable service architecture

Versioned, well-documented FastAPI endpoints

The system is intentionally designed to prioritize clarity, predictability, and trust over black-box behavior.

Why This Project Exists

Developers typically discover learning resources via search engines, which are poorly optimized for:

Skill relevance (e.g. data vs backend)

Learning intent (tools vs docs vs courses)

Source authority and trust

Explainability of why a resource is ranked higher

This project solves those gaps by providing:

Structured discovery by skill and intent

Deterministic ranking you can reason about

ML enhancement without risking system stability

Clear signals explaining ranking decisions

Core Capabilities

Skill-based resource discovery

Deterministic, explainable ranking (baseline)

Optional ML ranking with enforced fallback

Explicit Demo vs Full access modes

Pagination and filtering

Versioned REST API

Docker-ready deployment

Swagger UI documentation

Demo vs Full Access Model (Key Update)
Demo Mode (Default)

Designed for public exploration, previews, and safe sharing.

Characteristics:

Uses deterministic ranking only

No ML dependency

Stable, repeatable results

Results may be capped or shaped

score field intentionally omitted or null

Response explicitly reports:

"mode": "demo",
"ranking_mode": "deterministic"


Demo mode allows users to:

Explore the system safely

Understand ranking behavior

Interact with the API without credentials or ML artifacts

Full Mode

Designed for internal use, private deployments, or paid access.

Characteristics:

Enables ML ranking when available

Automatically falls back to deterministic scoring if ML is missing

Includes numeric score values

Full pagination support

Response explicitly reports ranking source:

"mode": "full",
"ranking_mode": "ml"


or

"ranking_mode": "deterministic"


Important:
ML is never silently assumed. The API always tells clients exactly what ranking logic was used.

Key Concepts
Skill Cluster

High-level developer domains:

backend

frontend

data

devops

mobile

Resource Type

The form of the learning material:

tool

documentation

course

article

repository

Domain Weight

A deterministic authority signal assigned during enrichment.

Higher = more trusted / established domain

Used as a primary ranking signal

Fully explainable and inspectable

Architecture Overview
API (FastAPI)
│
├── Routes        → HTTP interface & validation
├── Services      → Business logic orchestration
├── Ranking       → ML vs deterministic enforcement
├── Scoring       → Transparent heuristic logic
├── Demo Layer    → Controlled demo output shaping
├── ML Layer      → Optional trained model
├── Database      → SQLite (read-only, seeded)
└── ETL Pipeline  → Extract → Transform → Enrich


Design Principles:

Predictable behavior

Explicit control flow

Safe extensibility

Clear separation of concerns

API Endpoints (v1)
Health

GET /v1/health

Discovery

GET /v1/skills

GET /v1/resource-types

GET /v1/domains

GET /v1/stats

Debugging

GET /v1/debug/availability

Shows valid skill → resource_type combinations.

Recommendations

GET /v1/recommendations

Required

skill

Optional

limit

offset

resource_type

min_domain_weight

### Environment Variables

This project uses environment variables for sensitive configuration.

Required variables:
- `API_KEY` – Enables full (non-demo) access when provided

Example:
```bash
export API_KEY=your_key_here


access_mode (demo | full)

Example:

/v1/recommendations?skill=data&resource_type=tool&access_mode=demo

Tech Stack

FastAPI

Pydantic

SQLAlchemy

SQLite

Uvicorn

Docker

Pytest

Joblib (ML loading)

Project Status

 Production-ready
 Fully tested
 Explainable
 ML-extensible
 Portfolio-grade