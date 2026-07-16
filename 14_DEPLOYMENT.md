
# Deployment Guide

## Overview

This document describes how the Automated Single-Image to 3D Asset and Point Cloud Generation System will be deployed in Development, Testing, and Production environments.

The deployment architecture separates the frontend, backend, AI inference pipeline, and storage for better scalability and maintainability.

---

# Deployment Architecture

    User
                      │
                      ▼
             Next.js Frontend
                      │
                REST API
                      │
                      ▼
              FastAPI Backend
                      │
                      ▼
            AI Pipeline Manager
                      │
     ┌────────────────┼────────────────┐
     ▼                ▼                ▼
 Florence-2    GroundingDINO      SAM2.1
     │                │                │
     └────────────────┼────────────────┘
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

---

# Deployment Environments

## Development

Purpose

- Local development
- Feature implementation
- Debugging

Components

- Next.js Development Server
- FastAPI Development Server
- Local GPU
- Local File Storage

---

## Testing

Purpose

- Integration testing
- Performance testing
- Bug fixing

Components

- Next.js
- FastAPI
- GPU
- Automated Testing

---

## Production

Purpose

- End users

Components

- Reverse Proxy
- Frontend
- Backend
- AI Worker
- Storage
- Logging

---

# Recommended Production Architecture

Internet

↓

Nginx

↓

Next.js

↓

FastAPI

↓

Pipeline Worker

↓

GPU

↓

Outputs

---

# Frontend Deployment

Framework

Next.js

Deployment Options

- Vercel
- Docker
- Self Hosted

Recommended

Docker

---

# Backend Deployment

Framework

FastAPI

Server

Uvicorn

Process Manager

Gunicorn

Deployment

Docker Container

---

# AI Worker

Purpose

Runs the complete AI pipeline.

Responsibilities

- Load AI models
- Execute pipeline
- Generate outputs
- Save outputs

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

Object Storage

Examples

- AWS S3
- Azure Blob Storage
- MinIO

---

# Logging

Logs

```
logs/

pipeline.log

backend.log

errors.log
```

Log Rotation

Enabled

---

# Environment Variables

Example

```env
APP_ENV=production

HOST=0.0.0.0

PORT=8000

CUDA_DEVICE=0

LOG_LEVEL=INFO

OUTPUT_DIR=outputs

TEMP_DIR=data/temp
```

---

# Reverse Proxy

Recommended

Nginx

Responsibilities

- HTTPS
- Compression
- Static files
- Reverse proxy
- Security headers

---

# HTTPS

SSL Certificate

Let's Encrypt

HTTPS Required

Yes

---

# Docker

Recommended Containers

Container 1

Frontend

↓

Container 2

Backend

↓

Container 3

AI Worker

↓

Shared Output Volume

---

# Startup Order

1

Backend

↓

2

Frontend

↓

3

AI Worker

↓

4

Health Check

↓

Ready

---

# Health Monitoring

API

```
GET /api/v1/health
```

Expected

```json
{
    "status":"healthy"
}
```

---

# Backup

Backup

Configuration

Logs

Database (future)

Generated files (optional)

---

# Security

- HTTPS
- Input Validation
- File Size Limits
- Allowed File Types
- Secure Headers
- Rate Limiting (future)

---

# Performance Optimization

- Lazy model loading
- Sequential GPU execution
- Automatic GPU memory cleanup
- Temporary file cleanup
- Image validation before inference

---

# Monitoring

Monitor

- CPU Usage
- RAM Usage
- GPU Usage
- VRAM Usage
- Disk Usage
- Pipeline Time
- Error Rate

---

# Failure Recovery

If a stage fails

↓

Log Error

↓

Clean Temporary Files

↓

Return Failure Status

↓

Allow User Retry

---

# Deployment Checklist

Backend Running

Frontend Running

GPU Detected

CUDA Available

Models Downloaded

Output Directories Created

Logs Working

API Accessible

HTTPS Enabled

Health Check Passing

---

# Production Recommendations

- Use Docker for deployment.
- Keep AI inference on a dedicated GPU machine.
- Serve the frontend separately from the backend.
- Store only metadata in the database (if added later).
- Clean temporary files after each completed job.
- Monitor GPU memory to avoid out-of-memory errors.
