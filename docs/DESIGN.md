# Store Intelligence Platform - System Design

## Overview

The Store Intelligence Platform is a computer vision and analytics system designed to transform retail CCTV footage into actionable business intelligence.

The system detects visitors in real time, tracks their movement across store zones, generates behavioral events, stores them in PostgreSQL, and exposes analytics through REST APIs.

---

# High-Level Architecture

```text
Store Video
     │
     ▼
YOLOv8 Person Detection
     │
     ▼
ByteTrack Multi-Object Tracking
     │
     ▼
Zone Assignment Engine
     │
     ▼
Dwell Time Calculation
     │
     ▼
Event Generator
     │
     ▼
PostgreSQL
     │
     ▼
FastAPI Analytics Layer
     │
     ▼
Business Intelligence APIs
```

---

# Component Design

## 1. Detection Layer

### Purpose

Detect people inside the retail environment.

### Implementation

* Model: YOLOv8n
* Framework: Ultralytics
* Detection Class: PersonDetector

### Output

```json
{
  "person_id": 1,
  "bbox": [x1, y1, x2, y2],
  "confidence": 0.92
}
```

### Reasoning

YOLOv8n provides fast inference while maintaining sufficient accuracy for retail analytics use cases.

---

## 2. Tracking Layer

### Purpose

Maintain a persistent identity for each visitor across frames.

### Implementation

* Tracker: ByteTrack
* Component: VisitorTracker

### Output

```json
{
  "tracker_id": 5,
  "bbox": [...]
}
```

### Benefits

* Stable visitor IDs
* Reduced double counting
* Enables dwell time calculation

---

## 3. Zone Intelligence Layer

### Purpose

Determine which business zone a visitor occupies.

### Zones

* SKINCARE_ZONE
* DERMA_ZONE

### Logic

Bounding box center point is calculated:

```text
center_x = (x1 + x2) / 2
center_y = (y1 + y2) / 2
```

The center point is mapped to a predefined business zone.

### Output

```json
{
  "visitor_id": 5,
  "zone": "DERMA_ZONE"
}
```

---

## 4. Dwell Time Engine

### Purpose

Measure how long a visitor spends in a zone.

### Logic

For each tracked visitor:

```text
dwell_time =
current_time - first_seen_time
```

### Output

```json
{
  "visitor_id": 5,
  "zone": "DERMA_ZONE",
  "dwell_seconds": 24
}
```

---

## 5. Event Generation Layer

### Purpose

Convert raw tracking data into business events.

### Supported Events

* ENTRY
* ZONE_VISIT
* ZONE_CHANGE
* PURCHASE

### Example

```json
{
  "visitor_id": "5",
  "event_type": "ZONE_VISIT",
  "zone": "DERMA_ZONE"
}
```

### Benefits

Business logic is isolated from computer vision logic.

---

# Data Storage Layer

## PostgreSQL

All generated events are stored in PostgreSQL.

### Events Table

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

### Example Record

```json
{
  "event_type": "ZONE_VISIT",
  "event_metadata": {
    "zone": "DERMA_ZONE"
  }
}
```

---

# Analytics Layer

## FastAPI

FastAPI exposes all business intelligence endpoints.

### Core APIs

#### Event Ingestion

```http
POST /events/ingest
```

Features:

* Batch ingestion
* Idempotency
* Duplicate detection

---

#### Funnel Analytics

```http
GET /analytics/funnel
```

Returns:

* Entry count
* Purchase count
* Conversion rate

---

#### Zone Performance

```http
GET /analytics/zone-performance
```

Returns:

* Visits per zone
* Unique visitors

---

#### Heatmap

```http
GET /stores/{id}/heatmap
```

Returns:

* Zone frequency
* Visitor concentration

---

#### Anomaly Detection

```http
GET /stores/{id}/anomalies
```

Supported anomalies:

* Dead Zone
* Queue Spike
* Low Traffic

---

#### Health Monitoring

```http
GET /health
```

Returns:

* Service status
* Last event timestamp
* Stale feed detection
* Total event count

---

# Event Flow

```text
Video Frame
      │
      ▼
Person Detection
      │
      ▼
Tracking
      │
      ▼
Zone Assignment
      │
      ▼
Dwell Time
      │
      ▼
Event Generation
      │
      ▼
PostgreSQL
      │
      ▼
Analytics APIs
```

---

# Scalability Considerations

### Horizontal API Scaling

FastAPI instances can be replicated behind a load balancer because business state is stored in PostgreSQL.

### Camera Expansion

Multiple cameras can publish events to the same ingestion endpoint.

### Zone Expansion

Additional business zones can be configured without modifying the analytics layer.

---

# Reliability Features

* Structured logging middleware
* Health monitoring endpoint
* Stale feed detection
* Idempotent event ingestion
* PostgreSQL persistence
* Automated test coverage (81%)

---

# Testing Strategy

Automated tests validate:

* Health endpoint
* Event ingestion
* Funnel analytics
* Heatmap analytics
* Anomaly detection

Current coverage:

```text
81%
```

---

# Conclusion

The Store Intelligence Platform follows an event-driven architecture that separates computer vision, business logic, persistence, and analytics concerns. This design enables real-time visitor intelligence while remaining scalable, testable, and production-ready.
