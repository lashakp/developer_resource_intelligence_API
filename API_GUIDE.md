\# Developer Resource Intelligence API – Usage Guide



\## Overview

This API provides deterministic recommendations for developer learning resources

based on skill focus, resource type, domain authority, and quality signals.



---



\## Core Concepts



\### Skill Cluster

A skill cluster represents a broad technical area.



Examples:

\- `frontend` – UI, accessibility, performance

\- `backend` – APIs, servers, authentication

\- `data` – databases, analytics, data tooling

\- `devops` – CI/CD, infrastructure, cloud

\- `mobile` – iOS, Android, cross-platform



Use `/v1/skills` to see all available clusters.



---



\### Resource Type

Describes the nature of the resource.



Common values:

\- `tool` – software, platforms, utilities

\- `documentation` – official docs or guides

\- `course` – structured learning material

\- `repository` – GitHub or open-source projects

\- `article` – blog posts or written guides



Use `/v1/resource-types` to see available types.



---



\### Domain

The website hosting the resource (e.g. `aws.amazon.com`).



Domains help assess authority and reputation.



Use `/v1/domains` to explore known domains.



---



\### Domain Weight

A numeric authority signal assigned during enrichment.



Interpretation:

\- Higher = more authoritative / widely trusted

\- Lower = niche or less established



Domain weight is used in ranking and scoring.



---



\## Recommendations



\### Basic Recommendation

```http

GET /v1/recommendations?skill=data



