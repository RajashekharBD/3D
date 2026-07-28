
# Database Design

## Overview

The system uses Supabase (PostgreSQL) as its database backend, providing:

- Job Tracking
- Processing Status
- Output Metadata
- Error Logs
- User Management
- Authentication

The database should **not store AI model weights or generated files**. Those remain on disk (or object storage). The database stores only metadata.

---

# Database Technology

Database

Supabase (PostgreSQL)

Client Library

supabase-py

Auth

Supabase Auth (built-in)

Migration Tool

Supabase CLI

---

# Database Architecture

```
Frontend (Next.js)
      │
      ├── Supabase JS SDK (auth)
      │
      ▼
FastAPI Backend
      │
      ▼
supabase-py Client
      │
      ▼
Supabase PostgreSQL
```

---

# Entity Relationship Diagram

```
auth.users
   │
   │ (1:1)
   ▼
profiles
   │
   │ (1:N)
   ▼
jobs
   │
   │ (1:N)
   ▼
artifacts
```

---

# Table 1 — Profiles

Purpose

Stores application user profiles synced with Supabase Auth.

| Column     | Type        |
| ---------- | ----------- |
| id         | UUID (PK)   |
| email      | TEXT        |
| created_at | TIMESTAMPTZ |
| updated_at | TIMESTAMPTZ |
| last_login | TIMESTAMPTZ |

Auto-created via trigger on `auth.users` insert.

---

# Table 2 — Jobs

Purpose

Stores one record for every pipeline execution.

| Column                     | Type           |
| -------------------------- | -------------- |
| job_id                     | UUID (PK)      |
| user_id                    | UUID (FK)      |
| original_filename          | TEXT           |
| original_image_url         | TEXT           |
| thumbnail_url              | TEXT           |
| status                     | TEXT           |
| started_at                 | TIMESTAMPTZ    |
| completed_at               | TIMESTAMPTZ    |
| processing_duration_seconds| DOUBLE PRECISION|
| model_generated            | BOOLEAN        |
| pointcloud_generated       | BOOLEAN        |
| pipeline_version           | VARCHAR(20)    |
| error_message              | TEXT           |
| processing_device          | TEXT           |
| gpu_name                   | TEXT           |
| input_width                | INTEGER        |
| input_height               | INTEGER        |
| total_pipeline_time_ms     | BIGINT         |
| created_at                 | TIMESTAMPTZ    |
| updated_at                 | TIMESTAMPTZ    |
| is_deleted                 | BOOLEAN        |

Status Values

- uploaded
- processing
- completed
- failed

---

# Table 3 — Artifacts

Purpose

Stores metadata for files generated during pipeline execution.

| Column        | Type        |
| ------------- | ----------- |
| id            | UUID (PK)   |
| job_id        | UUID (FK)   |
| artifact_type | TEXT        |
| storage_path  | TEXT        |
| file_size     | BIGINT      |
| mime_type     | VARCHAR(100)|
| created_at    | TIMESTAMPTZ |

Artifact Types

- original, enhanced, detection, part_detection, mask
- segmentation, mask_overlay, rgba, model, pointcloud
- segmented_pointcloud, caption, grounding_prompt, result

---

# Indexes

Jobs

- idx_jobs_user (user_id)
- idx_jobs_created (created_at DESC)
- idx_jobs_status (status)
- idx_jobs_user_status_created (user_id, status, created_at DESC)

Artifacts

- idx_artifacts_job (job_id)
- UNIQUE (job_id, artifact_type)

Profiles

- idx_profiles_email_unique (email)

---

# Row Level Security

All tables have RLS enabled and forced.

Profiles

- SELECT / UPDATE: own profile only (auth.uid() = id)

Jobs

- SELECT: own non-deleted jobs (user_id = auth.uid() AND is_deleted = FALSE)
- INSERT / UPDATE / DELETE: own jobs only

Artifacts

- SELECT / INSERT / UPDATE / DELETE: artifacts linked to own jobs via subquery

---

# Triggers

update_updated_at_column

Auto-updates `updated_at` on row modification (profiles, jobs).

handle_new_user

On `auth.users` INSERT — auto-creates profile row.

handle_user_login

On `auth.users.last_sign_in_at` UPDATE — syncs `last_login`.

---

# Storage Buckets

- `original-images` (Private): Raw uploads
- `reconstruction-artifacts` (Private): GLBs, point clouds, masks, captions

---

# Job Lifecycle

```
Upload
  ↓
uploaded
  ↓
processing
  ↓
completed
  OR
failed
```

---

# Job Progress

| Stage              | Progress |
| ------------------ | -------- |
| Upload             | 0%       |
| Validation         | 5%       |
| Image Analysis     | 10%      |
| CLAHE              | 20%      |
| Florence-2         | 30%      |
| GroundingDINO      | 45%      |
| SAM2.1             | 60%      |
| Background Removal | 70%      |
| Hunyuan3D-2        | 85%      |
| Open3D             | 95%      |
| Completed          | 100%     |

---

# Error Recording

Every failure stores:

- Job ID
- Failed Stage
- Error Message
- Timestamp

Stored in `jobs.error_message` and `jobs.status = 'failed'`.

---

# File Storage

The database stores only file paths (as `storage_path` in artifacts).

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

# Migration File

```
supabase/migrations/20260717000000_auth_history_schema.sql
```

Run via Supabase CLI:

```bash
supabase migration up
```

---

# Database Summary

| Table     | Purpose                          |
| --------- | -------------------------------- |
| profiles  | User profiles (synced with auth) |
| jobs      | Pipeline execution tracking      |
| artifacts | Generated file metadata          |

---

# Design Principles

- Store metadata only
- Keep generated files on disk/object storage
- Use UUIDs for all primary keys
- RLS for multi-tenant isolation
- Soft-delete jobs (is_deleted flag)
- Minimize database writes during AI inference
- Mock/local fallback when Supabase is unavailable
