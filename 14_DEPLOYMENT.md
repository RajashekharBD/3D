
# Deployment Guide

## Overview

This document describes how the Automated Single-Image to 3D Asset and Point Cloud Generation System is deployed in Development, Testing, and Production environments.

The deployment architecture separates the frontend, backend, and storage for better scalability and maintainability.

---

# Deployment Architecture

```
    User
      │
      ▼
Next.js Frontend  (port 3000)
      │
 REST API (/api/v1)
      │
      ▼
FastAPI Backend   (port 8000)
      │
      ▼
 AI Pipeline Manager
      │
 ┌────┼────┐
 ▼    ▼    ▼
Florence-2 GroundingDINO SAM2.1
 │    │    │
 └────┼────┘
      ▼
 Background Removal
      ▼
  Hunyuan3D-2
      ▼
    Open3D
      ▼
    DBSCAN
      ▼
 Output Storage
```

---

# Docker Setup

Current architecture uses **2 services** (frontend + backend) defined in `docker-compose.yml`.

```
docker-compose.yml

services:
  backend:    FastAPI + AI pipeline, port 8000, GPU-enabled
  frontend:   Next.js, port 3000, depends on backend

volumes:
  shared-data
  shared-outputs
  shared-logs
```

**Note:** The `docker/` directory is reserved for future Dockerfiles. Currently empty.

---

# Startup Order

1. Backend (port 8000)
2. Frontend (port 3000)
3. Health Check (`GET /api/v1/health`)

---

# Health Monitoring

API

```
GET /api/v1/health
```

Expected

```json
{
    "status": "healthy"
}
```

---

# Environment Variables

```env
APP_ENV=production
HOST=0.0.0.0
PORT=8000
CUDA_DEVICE=0
LOG_LEVEL=INFO
OUTPUT_DIR=outputs
TEMP_DIR=data/temp
NEXT_PUBLIC_API_URL=http://backend:8000/api/v1
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

---

# Storage

Generated files

```
outputs/
  images/
  meshes/
  pointcloud/
  metadata/
```

Future

Object Storage (AWS S3, Azure Blob, MinIO)

---

# Logging

```
logs/
  pipeline.log
  backend.log
  errors.log
```

Log rotation enabled.

---

# Security

- Input Validation
- File Size Limits (25MB)
- Allowed File Types (jpg, png, webp)
- Secure Headers

---

# Performance Optimization

- Lazy model loading
- Sequential GPU execution
- Automatic GPU memory cleanup
- Temporary file cleanup
- Image validation before inference

---

# Failure Recovery

If a stage fails:

1. Log Error
2. Clean Temporary Files
3. Return Failure Status
4. Allow User Retry

---

# Production Recommendations

- Use Docker for deployment.
- Keep AI inference on a dedicated GPU machine.
- Serve the frontend separately from the backend.
- Store only metadata in the database (if added later).
- Clean temporary files after each completed job.
- Monitor GPU memory to avoid out-of-memory errors.
- Add reverse proxy (Nginx/Caddy) for production HTTPS termination.
