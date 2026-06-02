# Engineering Decisions and Trade-offs

## Overview

This document explains the major engineering decisions made while building the Store Intelligence Platform. For each component, alternatives were evaluated and a conscious trade-off was chosen based on the requirements of accuracy, simplicity, scalability, and implementation time.

---

# 1. Why YOLOv8n for Person Detection?

## Alternatives Considered

### YOLOv8n

Pros:

* Fast inference
* Low memory usage
* Easy deployment
* Sufficient accuracy for retail analytics

Cons:

* Lower accuracy than larger YOLO variants

---

### YOLOv8m / YOLOv8l

Pros:

* Better detection accuracy

Cons:

* Higher latency
* Larger model size
* Increased hardware requirements

---

## Decision

YOLOv8n was selected.

### Reasoning

The challenge focuses on visitor analytics rather than perfect object detection. Real-time processing and deployment simplicity were more important than marginal accuracy improvements.

---

# 2. Why ByteTrack for Multi-Object Tracking?

## Alternatives Considered

### ByteTrack

Pros:

* Lightweight
* High tracking accuracy
* Easy integration
* Strong performance in crowded scenes

Cons:

* Limited appearance-based matching

---

### DeepSORT

Pros:

* Appearance embeddings
* Better long-term re-identification

Cons:

* Additional neural network
* More compute intensive
* Increased complexity

---

## Decision

ByteTrack was selected.

### Reasoning

Retail visitors are continuously visible in most camera views. Re-identification across multiple cameras was not required. ByteTrack provides excellent performance with significantly lower complexity.

---

# 3. Why Event-Driven Architecture?

## Alternative

Directly calculate analytics from video frames.

### Problems

* Tight coupling between CV and analytics
* Difficult testing
* Difficult scaling
* Harder debugging

---

## Decision

Introduce an event generation layer.

### Example Events

```json
{
  "event_type": "ZONE_VISIT"
}
```

```json
{
  "event_type": "ZONE_CHANGE"
}
```

### Benefits

* Loose coupling
* Easier testing
* Historical analytics
* Replay capability
* Better scalability

---

# 4. Why PostgreSQL?

## Alternatives Considered

### PostgreSQL

Pros:

* ACID compliance
* Strong aggregation support
* JSON support
* Reliable analytics queries

Cons:

* Requires schema design

---

### MongoDB

Pros:

* Flexible schema

Cons:

* Aggregation complexity
* Less suitable for relational analytics

---

## Decision

PostgreSQL was selected.

### Reasoning

Most intelligence endpoints require aggregations, grouping, counting, and filtering. PostgreSQL provides strong support for these operations while still supporting JSON metadata fields.

---

# 5. Why FastAPI?

## Alternatives Considered

### FastAPI

Pros:

* Automatic OpenAPI documentation
* Pydantic validation
* High performance
* Type safety

Cons:

* Slight learning curve

---

### Flask

Pros:

* Simple and lightweight

Cons:

* Manual validation
* Manual API documentation
* More boilerplate

---

## Decision

FastAPI was selected.

### Reasoning

The challenge requires multiple APIs and structured request validation. FastAPI reduces development effort while improving reliability and documentation quality.

---

# 6. Why Store Events Instead of Raw Frames?

## Alternative

Store every video frame.

### Problems

* Massive storage requirements
* Expensive processing
* Difficult querying

---

## Decision

Store business events.

### Example

```json
{
  "visitor_id": "5",
  "event_type": "ZONE_VISIT",
  "zone": "DERMA_ZONE"
}
```

### Benefits

* Smaller storage footprint
* Faster analytics
* Easier reporting
* Better scalability

---

# 7. Why Zone-Based Analytics?

Retail managers are interested in:

* Which products attract visitors
* Which areas are underperforming
* Customer engagement by category

Zone-based analytics directly answer these business questions.

---

# 8. Why Dwell Time Tracking?

Visitor count alone is insufficient.

Two zones may receive the same number of visitors but generate very different engagement levels.

Dwell time helps identify:

* High-interest products
* Customer engagement
* Potential conversion opportunities

---

# 9. Why Idempotent Event Ingestion?

## Problem

Network retries can send the same event multiple times.

Without protection:

```text
ENTRY
ENTRY
ENTRY
```

would inflate analytics.

---

## Decision

Use event_id uniqueness validation.

Benefits:

* Safe retries
* Consistent metrics
* Production reliability

---

# 10. Why Health Monitoring?

Production systems require operational visibility.

The health endpoint provides:

* Service status
* Event volume
* Latest event timestamp
* Stale feed detection

This enables rapid troubleshooting and operational monitoring.

---

# Future Improvements

If additional development time were available:

1. Multi-camera visitor re-identification
2. Polygon-based zone definitions
3. Redis caching layer
4. Prometheus metrics
5. Grafana dashboards
6. Streaming event ingestion using Kafka
7. Advanced anomaly detection using historical baselines

---

# AI-Assisted Development Process

AI tools were used throughout development for brainstorming, debugging, code generation, documentation drafting, and test generation. All generated outputs were reviewed, modified, and validated before inclusion in the final implementation.

## Example 1: Detection Model Selection

AI initially suggested larger YOLO variants such as YOLOv8m to improve detection accuracy.

I selected YOLOv8n because the challenge prioritizes real-time retail analytics rather than object detection benchmarking. Lower inference latency and easier deployment were more valuable than marginal accuracy gains.

## Example 2: Tracking Strategy

AI suggested DeepSORT as an alternative tracker.

After evaluating the project requirements, I selected ByteTrack because the system operates on a single camera and does not require cross-camera re-identification. ByteTrack provided lower complexity and faster execution.

## Example 3: Dashboard Design

AI initially proposed a larger dashboard with many visualizations and metrics.

I simplified the dashboard to focus on operationally relevant information:

- Total Events
- Unique Visitors
- Zone Performance
- Health Status
- Active Anomalies

This improved readability and usability during demonstrations.

## Example 4: Anomaly Detection

AI suggested more advanced statistical anomaly detection approaches.

For the challenge scope, I implemented rule-based anomaly detection because it is explainable, easy to validate, and sufficient for demonstrating business intelligence capabilities.

## Validation Process

All generated code was manually reviewed and validated against real event data stored in PostgreSQL.

Validation included:

- API testing
- Database verification
- Dashboard verification
- Automated tests
- Coverage analysis
- End-to-end event flow validation

AI accelerated development, but all architectural decisions, trade-offs, testing, and final implementation choices were validated manually.

---

# Conclusion

The design prioritizes simplicity, reliability, and business value. Each technology choice was selected to maximize real-time retail intelligence while keeping the system maintainable, scalable, and production-ready.
