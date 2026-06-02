# Store Intelligence Platform

## Overview

Store Intelligence Platform is an event-driven retail analytics system that transforms CCTV video streams into actionable business insights.

The platform detects visitors using computer vision, tracks their movement across store zones, generates behavioral events, stores them in PostgreSQL, and exposes analytics through FastAPI endpoints.

Key capabilities include visitor tracking, zone analytics, dwell time analysis, funnel analytics, anomaly detection, heatmap generation, and operational health monitoring.

---

# Features

## Computer Vision Pipeline

* YOLOv8-based person detection
* ByteTrack multi-object tracking
* Zone assignment and visitor localization
* Dwell time computation
* Real-time event generation

## Event Intelligence

* ENTRY events
* ZONE_VISIT events
* ZONE_CHANGE events
* Purchase funnel support
* Event persistence in PostgreSQL

## Analytics APIs

* Event ingestion
* Funnel analytics
* Visitor analytics
* Hourly traffic analytics
* Zone performance analytics
* Heatmap analytics
* Store performance analytics
* Anomaly detection
* Health monitoring

## Production Readiness

* Dockerized deployment with Docker Compose
* PostgreSQL persistence
* Structured request logging
* Request tracing with trace IDs
* Health monitoring and stale-feed detection
* Idempotent event ingestion
* OpenAPI/Swagger API documentation
* Automated test suite
* 81% statement coverage

---

# System Architecture

```text
Video Stream
     │
     ▼
YOLOv8 Person Detection
     │
     ▼
ByteTrack Tracking
     │
     ▼
Zone Assignment
     │
     ▼
Dwell Time Engine
     │
     ▼
Event Generator
     │
     ▼
PostgreSQL Database
     │
     ▼
FastAPI Analytics Layer
     │
     ▼
Business Intelligence APIs
```

---

# Project Structure

```text
store-intelligence/
│
├── app/
│   ├── api/
│   │   ├── analytics.py
│   │   ├── anomalies.py
│   │   ├── funnel.py
│   │   ├── heatmap.py
│   │   ├── hourly_traffic.py
│   │   ├── ingest.py
│   │   ├── store_performance.py
│   │   ├── visitors.py
│   │   └── zone_performance.py
│   │
│   ├── database/
│   │   ├── base.py
│   │   ├── dependencies.py
│   │   └── session.py
│   │
│   ├── middleware/
│   │   └── logging_middleware.py
│   │
│   ├── models/
│   │   └── event.py
│   │
│   ├── repositories/
│   │   └── event_repository.py
│   │
│   ├── schemas/
│   │   ├── event.py
│   │   └── event_types.py
│   │
│   ├── logger.py
│   ├── config.py
│   └── main.py
│
├── pipeline/
│   ├── detector.py
│   ├── tracker.py
│   ├── dwell.py
│   ├── events.py
│   ├── zones.py
│   └── run_pipeline.py
│
├── dashboard/
│   └── app.py
│
├── tests/
│   ├── test_health.py
│   ├── test_ingest.py
│   ├── test_heatmap.py
│   ├── test_anomalies.py
│   └── test_funnel.py
│
├── docs/
│   ├── DESIGN.md
│   └── CHOICES.md
│
├── Dockerfile
├── .dockerignore
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .env
```


---

# Technology Stack

| Layer            | Technology            |
|------------------|----------------------|
| Detection        | YOLOv8               |
| Tracking         | ByteTrack            |
| Backend API      | FastAPI              |
| Database         | PostgreSQL           |
| ORM              | SQLAlchemy           |
| Validation       | Pydantic             |
| Testing          | Pytest               |
| Dashboard        | Streamlit            |
| Containerization | Docker & Docker Compose |
| Logging          | Python Logging       |

---


# Setup

## 1. Clone Repository

```bash
git clone <repository-url>
cd store-intelligence
```

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Start the Platform

```bash
docker compose up --build
```

This command starts:

- PostgreSQL
- FastAPI API Server

Health Endpoint:

```text
http://localhost:8000/health
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

# Running the Detection Pipeline

Execute the computer vision pipeline:

```bash
python -m pipeline.run_pipeline
```

Expected output:

```text
EVENT GENERATED:
ZONE_VISIT
```

Generated events are automatically stored in PostgreSQL.

---

# API Documentation

Interactive documentation:

```text
http://127.0.0.1:8000/docs
```

# Live Dashboard

The platform includes a real-time Streamlit dashboard connected directly to the analytics APIs.

Start the dashboard:

```bash
streamlit run dashboard/app.py
```

or

```bash
python -m streamlit run dashboard/app.py
```

Dashboard URL:

```text
http://localhost:8501
```

Dashboard Features:

- Real-time store metrics
- Zone performance analytics
- Health monitoring
- Live anomaly detection
- Visitor insights
- Operational visibility

### Running the Complete Platform

Terminal 1 — Start the API

```bash
docker compose up --build
```

Terminal 2 — Start the Detection Pipeline

```bash
python -m pipeline.run_pipeline
```

Terminal 3 — Launch the Dashboard

```bash
python -m streamlit run dashboard/app.py
```

The dashboard automatically refreshes and displays live metrics generated by the computer vision pipeline and analytics APIs.

---

# Available Endpoints

## Health

```http
GET /health
```

Returns:

```json
{
  "service": "store-intelligence",
  "status": "healthy",
  "stale_feed": false,
  "total_events": 71
}
```

---

## Event Ingestion

```http
POST /events/ingest
```

Supports:

* Batch ingestion
* Duplicate detection
* Idempotency validation

---

## Funnel Analytics

```http
GET /analytics/funnel
```

Returns:

* Entries
* Purchases
* Conversion rate

---

## Zone Performance

```http
GET /analytics/zone-performance
```

Returns:

* Visits by zone
* Visitor engagement

---

## Zone Summary

```http
GET /analytics/zone-summary
```

Returns:

* Total zone events
* Unique visitors

---

## Visitors Analytics

```http
GET /analytics/visitors
```

Returns:

* Visitor counts
* Visitor activity statistics

---

## Hourly Traffic

```http
GET /analytics/hourly-traffic
```

Returns:

* Traffic distribution by hour

---

## Store Performance

```http
GET /analytics/store-performance
```

Returns:

* Store-level operational metrics

---

## Heatmap Analytics

```http
GET /stores/{store_id}/heatmap
```

Returns:

* Zone popularity
* Visitor concentration

---

## Anomaly Detection

```http
GET /stores/{store_id}/anomalies
```

Supported anomalies:

* Dead Zone
* Low Traffic
* Queue Spike

---

# Database Schema

## Events Table

```text
event_id
visitor_id
store_id
camera_id
event_type
confidence
timestamp
event_metadata
```

Example:

```json
{
  "event_type": "ZONE_VISIT",
  "event_metadata": {
    "zone": "DERMA_ZONE"
  }
}
```

---

# Testing

Run all tests:

```bash
pytest -v
```

Run coverage:

```bash
pytest --cov=app --cov-report=term
```

Current results:

```text
5 tests passed
81% coverage
```

---
# Test Coverage & Quality Assurance

The project includes an automated test suite focused on validating business-critical functionality and analytics correctness.

## Covered APIs

- Health Monitoring API
- Event Ingestion API
- Funnel Analytics API
- Heatmap Analytics API
- Anomaly Detection API

## Coverage Metrics

```text
5 tests passed
81% statement coverage
```

This exceeds the challenge requirement of **70% minimum statement coverage**.

## Validated Scenarios

The automated tests verify:

- Health endpoint availability
- Event ingestion workflow
- Duplicate event detection
- Idempotent ingestion behavior
- Funnel analytics calculations
- Heatmap generation
- Anomaly detection logic
- Response validation

--- 

# Reliability Features

* Structured request logging
* Trace identifiers for observability
* Health monitoring endpoint
* Stale feed detection
* Idempotent event ingestion
* PostgreSQL persistence
* Automated testing
* 81% statement coverage
* Dockerized deployment
* OpenAPI schema validation

---

# Documentation

Additional project documentation:

```text
docs/DESIGN.md
```

Contains:

* System architecture
* Data flow
* Component interactions
* Scalability considerations

```text
docs/CHOICES.md
```

Contains:

* Engineering trade-offs
* Technology selection rationale
* Design decisions

---

# Future Improvements

* Multi-camera visitor re-identification
* Polygon-based zone definitions
* Stream processing with Kafka
* Redis caching
* Prometheus metrics
* Grafana dashboards
* Advanced anomaly detection models

---

# Results

* Real-time visitor detection and tracking
* Event-driven retail analytics
* Session-based funnel analytics
* Automated anomaly detection
* Dockerized production deployment
* OpenAPI-documented REST APIs
* 81% automated test coverage
* Structured observability and monitoring
* Live Streamlit dashboard with real-time KPI monitoring
* Single-command deployment using Docker Compose

---

# Acceptance Criteria Achieved

✅ Docker Compose starts the complete platform

✅ Event ingestion endpoint accepts valid events

✅ Analytics APIs return valid JSON responses

✅ Structured logging and trace IDs implemented

✅ Health monitoring endpoint available

✅ Automated tests passing

✅ 81% statement coverage

✅ DESIGN.md included

✅ CHOICES.md included

✅ Live Streamlit dashboard implemented

--- 

# Submission Highlights

- End-to-end retail analytics platform
- YOLOv8 + ByteTrack visitor tracking pipeline
- Event-driven architecture with PostgreSQL
- FastAPI analytics layer with OpenAPI documentation
- Streamlit live monitoring dashboard
- Structured logging and health monitoring
- Idempotent event ingestion
- Automated anomaly detection
- Dockerized deployment
- 81% automated test coverage

---

# Author

Shrey Srivastava

B.Tech Artificial Intelligence & Machine Learning

Store Intelligence Platform – Retail Analytics and Computer Vision System
