
# Backend API Specification

## Overview

The backend is responsible for:

- Receiving user uploads
- Managing AI pipeline execution
- Tracking job status
- Managing output files
- Returning generated assets

The backend is implemented using **FastAPI** and exposes REST APIs consumed by the frontend.

---

# API Architecture

```
Next.js Frontend
        │
        ▼
 REST API (FastAPI)
        │
        ▼
 Pipeline Manager
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

Current Version

No Authentication

Future

JWT Authentication

---

# Response Format

Success

```json
{
    "success": true,
    "message": "Operation completed",
    "data": {}
}
```

Failure

```json
{
    "success": false,
    "message": "Error description",
    "error": {}
}
```

---

# API 1

## Health Check

GET

```
/health
```

Purpose

Check server status.

Response

```json
{
  "status":"healthy"
}
```

---

# API 2

## Upload Image

POST

```
/upload
```

Request

Multipart Form Data

Field

```
image
```

Supported

- JPG
- JPEG
- PNG
- WEBP
- BMP

Response

```json
{
  "job_id":"abc123"
}
```

---

# API 3

## Start Pipeline

POST

```
/pipeline/start/{job_id}
```

Purpose

Starts complete AI pipeline.

Stages

- Validation
- Enhancement
- Detection
- Segmentation
- Background Removal
- 3D Generation
- Point Cloud
- Export

Response

```json
{
    "status":"started"
}
```

---

# API 4

## Pipeline Status

GET

```
/pipeline/status/{job_id}
```

Example Response

```json
{
  "job_id":"abc123",

  "status":"running",

  "stage":"GroundingDINO",

  "progress":38
}
```

Possible Status

Queued

Running

Completed

Failed

Cancelled

---

# API 5

## Pipeline Result

GET

```
/pipeline/result/{job_id}
```

Response

```json
{
    "status":"completed",

    "outputs":{

        "detection_image":"...",

        "segmentation_image":"...",

        "rgba":"...",

        "glb":"...",

        "pointcloud":"...",

        "segmented_pointcloud":"..."
    }
}
```

---

# API 6

## Download GLB

GET

```
/download/glb/{job_id}
```

Returns

GLB File

---

# API 7

## Download Point Cloud

GET

```
/download/pointcloud/{job_id}
```

Returns

PLY File

---

# API 8

## Download RGBA Image

GET

```
/download/rgba/{job_id}
```

Returns

PNG

---

# API 9

## Download Detection Image

GET

```
/download/detection/{job_id}
```

---

# API 10

## Download Segmentation Image

GET

```
/download/segmentation/{job_id}
```

---

# API 11

## Download Metadata

GET

```
/download/report/{job_id}
```

Returns

JSON

---

# API 12

## Delete Job

DELETE

```
/jobs/{job_id}
```

Purpose

Delete temporary files.

---

# Pipeline Progress

0%

Upload Complete

↓

5%

Validation

↓

10%

Image Analysis

↓

15%

CLAHE

↓

25%

Florence-2

↓

40%

GroundingDINO

↓

50%

Part Detection

↓

60%

SAM2.1

↓

70%

Background Removal

↓

80%

Hunyuan3D Shape

↓

90%

Texture Generation

↓

95%

Point Cloud

↓

100%

Completed

---

# HTTP Status Codes

200

Success

201

Created

400

Bad Request

404

Not Found

422

Validation Error

500

Internal Error

---

# File Limits

Maximum Upload

25 MB

Supported Formats

JPG

JPEG

PNG

WEBP

BMP

---

# Output Files

```
outputs/

images/

meshes/

pointcloud/

metadata/
```

---

# Error Response

Example

```json
{
  "success":false,

  "message":"GroundingDINO detection failed.",

  "stage":"GroundingDINO"
}
```

---

# API Flow

```
Upload Image

↓

Receive Job ID

↓

Start Pipeline

↓

Check Status

↓

Pipeline Complete

↓

Download Outputs
```

---

# Backend Modules

```
Upload API

↓

Pipeline Manager

↓

AI Model Manager

↓

Mesh Generator

↓

Point Cloud Generator

↓

Export Manager
```

---

# Logging

Each request stores

- Job ID
- Request Time
- Pipeline Stage
- Processing Time
- Errors
- Output Files

---

# API Versioning

Current

```
v1
```

Future

```
v2
```

Backward compatibility will be maintained.

---

# Future APIs

Future versions may include:

- Batch image processing
- Multiple object reconstruction
- User authentication
- Project history
- Cloud storage integration
- WebSocket live progress
