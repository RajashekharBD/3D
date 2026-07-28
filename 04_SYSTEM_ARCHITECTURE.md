
# System Architecture

## Overview

The Automated Single-Image to 3D Asset and Point Cloud Generation System follows a modular, sequential, AI-driven architecture. Each stage performs a single well-defined task and passes its output to the next stage. This design improves maintainability, debugging, scalability, and future extensibility.

---

# High-Level Architecture

    User
                      │
                      ▼
              Upload Image
                      │
                      ▼
           FastAPI Backend Server
                      │
                      ▼
       AI Processing Pipeline Engine
                      │
      ┌───────────────┴───────────────┐
      ▼                               ▼
Image Processing               AI Inference
      │                               │
      └───────────────┬───────────────┘
                      ▼
            3D Reconstruction
                      │
                      ▼
          Point Cloud Generation
                      │
                      ▼
         Point Cloud Segmentation
                      │
                      ▼
              Output Generation
                      │
                      ▼
                Next.js Frontend

---

# Complete Processing Pipeline

Input Image
      │
      ▼
────────────────────────────────────
Stage 1
Image Analysis
────────────────────────────────────
      │
      ▼
Brightness Detection

Contrast Detection

Resolution Validation

    │
      ▼
CLAHE Enhancement
(only if required)

    │
      ▼
────────────────────────────────────
Stage 2
Automatic Caption Generation
────────────────────────────────────

Florence-2

    │
      ▼
Caption

Example

"A black ceramic mug"

    │
      ▼
Prompt Generation

black . ceramic . mug

    │
      ▼
────────────────────────────────────
Stage 3
Object Detection
────────────────────────────────────

GroundingDINO

    │
      ▼
Bounding Boxes

    │
      ▼
Detection Retry Strategy

Pass 1

Original Image

↓

Pass 2

Enhanced Image

↓

Pass 3

Lower Threshold

↓

Pass 4

Final Retry

    │
      ▼
────────────────────────────────────
Stage 4
Part Detection
────────────────────────────────────

Florence-2

    │
      ▼
Body

Handle

Wheel

Door

etc.

    │
      ▼
────────────────────────────────────
Stage 5
Instance Segmentation
────────────────────────────────────

SAM2.1

    │
      ▼
Binary Masks

Highest IoU Mask

Object Mask

    │
      ▼
────────────────────────────────────
Stage 6
Background Removal
────────────────────────────────────

rembg

↓

RGBA Image

Transparent Background

    │
      ▼
────────────────────────────────────
Stage 7
3D Reconstruction
────────────────────────────────────

Hunyuan3D-2

Stage 1

↓

Shape Generation

↓

Stage 2

Texture Generation

↓

GLB Mesh

    │
      ▼
────────────────────────────────────
Stage 8
Mesh Processing
────────────────────────────────────

Open3D

↓

Mesh Validation

↓

Normal Computation

    │
      ▼
────────────────────────────────────
Stage 9
Point Cloud Generation
────────────────────────────────────

Poisson Disk Sampling

↓

Point Cloud

↓

Surface Normals

    │
      ▼
────────────────────────────────────
Stage 10
Point Cloud Segmentation
────────────────────────────────────

DBSCAN

↓

Clusters

↓

Colored Point Cloud

    │
      ▼
────────────────────────────────────
Stage 11
Export
────────────────────────────────────

Detection Image

↓

Segmented Image

↓

RGBA Image

↓

GLB

↓

PLY

↓

Metadata

---

# Module Architecture

Module 1

Image Upload

Input

User Image

Output

RGB Image

---

Module 2

Image Enhancement

Input

RGB Image

Output

Enhanced Image

Technology

OpenCV

---

Module 3

Caption Generation

Input

Image

Output

Caption

Technology

Florence-2

---

Module 4

Object Detection

Input

Caption

Image

Output

Bounding Boxes

Technology

GroundingDINO

---

Module 5

Part Detection

Input

Detected Object

Output

Part Bounding Boxes

Technology

Florence-2

---

Module 6

Segmentation

Input

Bounding Boxes

Output

Binary Masks

Technology

SAM2.1

---

Module 7

Background Removal

Input

Object Mask

Output

RGBA Image

Technology

rembg

---

Module 8

3D Reconstruction

Input

RGBA Image

Output

GLB

Technology

Hunyuan3D-2

---

Module 9

Point Cloud Generation

Input

GLB

Output

PLY

Technology

Open3D

---

Module 10

Point Cloud Segmentation

Input

PLY

Output

Clustered PLY

Technology

DBSCAN

---

# Backend Architecture

Client

↓

FastAPI

↓

JWT Auth Middleware

↓

Controller

↓

Pipeline Manager

↓

Image Module

↓

Detection Module

↓

Segmentation Module

↓

3D Module

↓

Point Cloud Module

↓

Export Module

---

# JWT Authentication

All API routes (except `/api/v1/health`) require JWT authentication.

The `get_current_user` dependency in `core/auth.py` performs:

1. Extract token from `Authorization: Bearer` header or `token` query parameter
2. Verify token against Supabase Auth API (`/auth/v1/user`)
3. Return user dict with `id` and `email`
4. Fall back to mock user if `SUPABASE_JWT_SECRET` is not configured (local development)

Routes authenticate via FastAPI dependency injection in the controller layer.

---

# Database Sync

The system syncs job state to Supabase via the `Database` class in `core/database.py`.

- Jobs table: `job_id`, `user_id`, `status`, `original_filename`, `processing_duration_seconds`, `created_at`, `completed_at`
- Artifacts table: `job_id`, `artifact_type`, `storage_path`, `file_size`, `mime_type`
- Profiles table: `id`, `email`, `last_login`

Database syncing is optional: if Supabase credentials are not configured, the system operates in local/mock mode using only the filesystem for state.

---

# Background Task Execution

Pipeline execution is asynchronous. The upload endpoint uses FastAPI's `BackgroundTasks` to offload the full reconstruction pipeline.

Flow:

1. `POST /api/v1/upload` receives image and validates it synchronously
2. Returns `job_id` immediately with status `processing`
3. Pipeline runs in background via `BackgroundTasks.add_task(execute_full_reconstruction_pipeline, job_id, original_png_path)`
4. Frontend polls `GET /api/v1/pipeline/{job_id}/status` to track progress
5. Status is computed from `result.json` in the job's output directory

---

# Frontend Architecture

User

↓

Next.js App Router

↓

Pages

├── Landing (/)

├── Upload (/upload)

├── Processing (/processing/[jobId])

├── Results (/results/[jobId])

├── Viewer (/viewer)

├── Download (/download)

├── History (/history)

├── Profile (/profile)

├── Login (/login)

├── Signup (/signup)

└── Forgot Password (/forgot-password)

↓

React Components

├── Auth (LoginForm, SignupForm, ForgotPasswordForm, ProtectedRoute)

├── Download (DownloadPanel)

├── Footer (Footer)

├── History (HistoryGrid, HistoryCard, SearchBar, SortMenu)

├── Navbar (Navbar)

├── Profile (ProfileCard, StatisticsCard)

├── Progress (ProgressTracker)

└── ThreeViewer

↓

Context & Utils

├── AuthContext (Supabase auth state management)

└── supabaseClient (Supabase client initialization)

---

# Data Flow

User Upload

↓

Image

↓

Enhanced Image

↓

Caption

↓

Prompt

↓

Bounding Boxes

↓

Masks

↓

RGBA Image

↓

3D Mesh

↓

Point Cloud

↓

Segmented Point Cloud

↓

Downloads

---

# Error Handling

The system uses a custom exception hierarchy defined in `core/exceptions.py`:

- `BaseAppException` — base class with `status_code`, `message`, and optional `stage`
- `ImageValidationError` — 400 errors for invalid uploads (empty file, bad format, corrupt, too large)
- `PipelineError` — 500 errors during pipeline execution tagged with the failing stage
- `NoObjectDetected` — 422 error when detection fails on all retries

The `ExceptionHandlingMiddleware` in `middleware/exception_middleware.py` catches all exceptions and returns consistent JSON responses:

```json
{
  "success": false,
  "message": "Error description",
  "stage": "FailingStage"  // optional
}
```

Detection failures trigger retry with CLAHE-enhanced image and lowered thresholds before aborting.

---

# GPU Memory Management

Load Florence-2

↓

Inference

↓

Unload

↓

Clear CUDA Cache

↓

Load GroundingDINO

↓

Inference

↓

Unload

↓

Clear CUDA Cache

↓

Load SAM2.1

↓

Inference

↓

Unload

↓

Clear CUDA Cache

↓

Load Hunyuan3D-2

↓

Inference

↓

Unload

↓

Clear CUDA Cache

This sequential loading minimizes GPU memory usage and enables execution on GPUs with limited VRAM. Hunyuan3D-2 additionally uses `cpu_offload`, `sequential_cpu_offload`, `attention_slicing`, `vae_slicing`, and `vae_tiling` to further reduce peak VRAM.

---

# Output Files

outputs/

<job_id>/

- original.png

- result.json

- detection.png

- enhanced.png

- segmentation.png

- rgba.png

- grounding_prompt.txt

- caption.txt

- mask.png

- mask_overlay.png

- part_detection.png

- model.glb

- model.obj (optional, based on pipeline stage)

- pointcloud.ply

- segmented_pointcloud.ply

- preview.png

- scene.json (floor plan pipeline)

- debug/ (pipeline-specific debug artifacts)

---

# Design Principles

- Modular Architecture
- Single Responsibility Principle
- Loose Coupling
- High Cohesion
- GPU Memory Optimization
- Reusable Components
- Scalable Design
- Production Ready
- Fault Tolerant
- Easy Maintenance
