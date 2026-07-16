
# Database Design

## Overview

Although the first version of the project can run without a database, using a database provides:

- Job Tracking
- Processing Status
- Output Metadata
- Error Logs
- Performance Statistics
- Future User Management

The database should **not store AI model weights or generated files**. Those remain on disk (or object storage). The database stores only metadata.

---

# Database Technology

Development

SQLite

Production

PostgreSQL

ORM

SQLAlchemy

Migration Tool

Alembic

---

# Database Architecture

```
Frontend
      │
      ▼
FastAPI Backend
      │
      ▼
SQLAlchemy
      │
      ▼
PostgreSQL
```

---

# Entity Relationship Diagram

```
Job
 │
 ├── OutputFile
 │
 ├── PipelineLog
 │
 └── PerformanceMetrics
```

---

# Table 1 — Jobs

Purpose

Stores one record for every uploaded image.

| Column        | Type      |
| ------------- | --------- |
| id            | UUID      |
| filename      | VARCHAR   |
| original_name | VARCHAR   |
| status        | VARCHAR   |
| current_stage | VARCHAR   |
| progress      | INTEGER   |
| created_at    | TIMESTAMP |
| updated_at    | TIMESTAMP |
| completed_at  | TIMESTAMP |

Status Values

- Queued
- Running
- Completed
- Failed
- Cancelled

---

# Table 2 — Output Files

Purpose

Stores paths of generated outputs.

| Column               | Type |
| -------------------- | ---- |
| id                   | UUID |
| job_id               | UUID |
| detection_image      | TEXT |
| segmentation_image   | TEXT |
| rgba_image           | TEXT |
| glb_model            | TEXT |
| pointcloud           | TEXT |
| segmented_pointcloud | TEXT |
| metadata_json        | TEXT |

Relationship

Many Output Files

↓

One Job

---

# Table 3 — Pipeline Logs

Purpose

Stores execution history.

| Column      | Type      |
| ----------- | --------- |
| id          | UUID      |
| job_id      | UUID      |
| stage       | VARCHAR   |
| status      | VARCHAR   |
| duration_ms | INTEGER   |
| message     | TEXT      |
| created_at  | TIMESTAMP |

Example

```
Stage

GroundingDINO

Status

Completed

Duration

3920 ms
```

---

# Table 4 — Performance Metrics

Purpose

Stores execution performance.

| Column               | Type    |
| -------------------- | ------- |
| id                   | UUID    |
| job_id               | UUID    |
| upload_time_ms       | INTEGER |
| caption_time_ms      | INTEGER |
| detection_time_ms    | INTEGER |
| segmentation_time_ms | INTEGER |
| background_time_ms   | INTEGER |
| generation_time_ms   | INTEGER |
| pointcloud_time_ms   | INTEGER |
| total_time_ms        | INTEGER |

---

# Relationships

```
Job

↓

Output Files

↓

Pipeline Logs

↓

Performance Metrics
```

---

# Job Lifecycle

```
Upload

↓

Queued

↓

Running

↓

Completed

OR

Failed
```

---

# Job Progress

| Progress | Stage              |
| -------- | ------------------ |
| 0%       | Upload             |
| 5%       | Validation         |
| 10%      | Image Analysis     |
| 20%      | CLAHE              |
| 30%      | Florence-2         |
| 45%      | GroundingDINO      |
| 60%      | SAM2.1             |
| 70%      | Background Removal |
| 85%      | Hunyuan3D-2        |
| 95%      | Open3D             |
| 100%     | Completed          |

---

# Database Indexes

Jobs

- id
- status
- created_at

Pipeline Logs

- job_id
- stage

Output Files

- job_id

Performance Metrics

- job_id

---

# Data Retention

Temporary Files

Delete after

24 Hours

Database Records

Keep

30 Days

Logs

Keep

30 Days

---

# File Storage

The database stores only file paths.

Example

```
outputs/

images/

detection.png

meshes/

model.glb

pointcloud/

pointcloud.ply
```

---

# Error Recording

Every failure stores

- Job ID
- Failed Stage
- Error Message
- Stack Trace (optional)
- Timestamp

---

# Future Expansion

The schema supports future features without redesign:

- User Accounts
- Authentication
- Multiple Projects
- Batch Processing
- Cloud Storage
- Processing History
- Team Collaboration
- Project Sharing
- Analytics Dashboard

---

# Backup Strategy

Development

SQLite Backup

Production

Daily PostgreSQL Backup

---

# Database Summary

| Table              | Purpose                     |
| ------------------ | --------------------------- |
| Jobs               | Tracks pipeline execution   |
| OutputFiles        | Stores generated file paths |
| PipelineLogs       | Records stage execution     |
| PerformanceMetrics | Stores timing information   |

---

# Design Principles

- Store metadata only
- Keep generated files on disk/object storage
- Use UUIDs for all primary keys
- Track every pipeline stage
- Record execution times
- Support future scalability
- Minimize database writes during AI inference
