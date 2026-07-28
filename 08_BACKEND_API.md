
# Backend API Specification

## Overview

The backend is implemented using **FastAPI** and exposes REST APIs consumed by the Next.js frontend.

- Receiving user uploads
- Managing AI pipeline execution (background task)
- Tracking job status
- Managing output files and artifacts
- Returning generated assets

---

# Architecture

```
Next.js Frontend
      │
      ▼
  REST API (FastAPI) — /api/v1/*
      │
      ▼
  Controllers → Pipeline (BackgroundTasks)
      │
      ├── Image Processing
      ├── Florence-2
      ├── GroundingDINO
      ├── SAM2.1
      ├── rembg
      ├── Hunyuan3D-2
      ├── Open3D
      └── DBSCAN
```

---

# Base URL

Development

```
http://localhost:8000/api/v1
```

Production

```
https://your-domain.com/api/v1
```

---

# Authentication

All endpoints except `/api/v1/health` require **JWT authentication** via the `get_current_user` dependency.

- Reads `Authorization: Bearer <token>` header
- Verifies token against Supabase Auth API (`/auth/v1/user`)
- Falls back to `token` query parameter for direct downloads
- Returns mock user (`local_user@example.com`) when `SUPABASE_JWT_SECRET` is unset (development)

---

# Response Format

## Pipeline Status Response

```json
{
  "job_id": "abc123",
  "status": "running",
  "current_stage": "GroundingDINO Detection",
  "progress": 30,
  "completed_phases": ["upload", "validation", "analysis", "clahe", "caption_generation"],
  "artifacts": {"original": "original.png"}
}
```

## Upload Response

```json
{
  "job_id": "abc123"
}
```

## List Artifacts Response

```json
{
  "job_id": "abc123",
  "artifacts": {
    "model": true,
    "pointcloud": false,
    "segmented_pointcloud": false,
    "rgba": true,
    "detection": true,
    "segmentation": true
  }
}
```

## Error Response

```json
{
  "success": false,
  "message": "GroundingDINO detection failed.",
  "stage": "GroundingDINO"
}
```

---

# Endpoints

## 1. Health Check

```
GET /health
```

No authentication required.

Response: `{"status": "healthy"}`

---

## 2. Upload Image

```
POST /upload
```

**Auth**: Required

**Request**: Multipart form data, field `image`

Supported: JPG, JPEG, PNG, WEBP, BMP (max 25 MB)

**Response**: `{"job_id": "abc123"}`

Pipeline starts automatically as a **background task** after upload — no separate start endpoint.

---

## 3. Pipeline Status

```
GET /pipeline/status/{job_id}
```

**Auth**: Required

Returns current processing status and progress.

**Status values**: `processing`, `completed`, `failed`, `not_found`

**Progress** computed from completed phases (0–100).

---

## 4. List Artifacts

```
GET /download/{job_id}
```

**Auth**: Required

Returns availability map of all artifact keys.

**Artifact keys**: model, pointcloud, segmented_pointcloud, rgba, detection, segmentation, mask_overlay, result, original, enhanced, caption, grounding_prompt, part_detection, mask

---

## 5. Download Artifact

```
GET /download/{job_id}/{artifact_key}
```

**Auth**: Required (query param `?token=` also accepted for direct links)

Returns the file as a download attachment with appropriate `Content-Type`.

---

## 6. History — List Jobs

```
GET /history
```

**Auth**: Required

Query params: `filename`, `status`, `sort_by` (newest/oldest), `page`

Returns paginated job list for the authenticated user.

---

## 7. History — Job Detail

```
GET /history/{job_id}
```

**Auth**: Required

Returns full job record + associated artifacts.

---

## 8. History — Delete Job

```
DELETE /history/{job_id}
```

**Auth**: Required

Performs soft delete in database + removes local `outputs/<job_id>/` directory.

---

## 9. Profile

```
GET /profile
```

**Auth**: Required

Returns user profile info and usage statistics (total uploads, completed/failed jobs, models generated, etc.).

---

# Pipeline Progress

```
  0% — Upload
  5% — Validation
  8% — Image Analysis
 12% — CLAHE Enhancement
 16% — Florence-2 Captioning
 22% — GroundingDINO Detection
 30% — Florence-2 Part Detection
 36% — SAM2.1 Segmentation
 44% — Background Removal
 50% — Hunyuan3D-2 Shape Generation
 65% — Hunyuan3D-2 Texture Generation
 78% — Mesh Validation
 82% — Point Cloud Generation
 90% — DBSCAN Segmentation
 98% — Completed (100%)
```

Progress is calculated by the last completed phase in `result.json`.

---

# HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Error |

---

# File Limits

| Property | Value |
|----------|-------|
| Max Upload | 25 MB |
| Formats | JPG, JPEG, PNG, WEBP, BMP |

---

# Backend Modules

```
backend/app/
  api/          → Route definitions (health, upload, pipeline, download, history, profile)
  controllers/  → Business logic per endpoint
  pipeline/     → Stage execution (image, detection, segmentation, generation, pointcloud)
  services/     → Reusable services (storage, image, mesh, pointcloud)
  core/         → Settings, auth, database, exceptions, constants
  schemas/      → Pydantic response/request models
  middleware/   → Exception handling
  utils/        → Artifacts manager, validators, image/mesh/pointcloud utils
```
