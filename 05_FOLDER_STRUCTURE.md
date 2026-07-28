
# Project Folder Structure

## Overview

This document defines the actual folder structure of the Automated Single-Image to 3D Asset and Point Cloud Generation System.

The project follows a modular architecture where each AI model and processing stage is isolated into its own module. This improves maintainability, scalability, testing, and future expansion.

---

# Root Directory

```
single-image-3d-system/
│
├── backend/
├── frontend/
├── ai_models/
├── configs/
├── data/
├── outputs/
├── scripts/
├── docs/
├── tests/
├── logs/
├── docker/
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── README.md
└── LICENSE
```

---

# Backend

```
backend/
│
├── app/
│   ├── api/
│   ├── controllers/
│   ├── services/
│   ├── pipeline/
│   ├── models/        (empty)
│   ├── utils/
│   ├── schemas/
│   ├── middleware/
│   ├── core/
│   ├── config/        (empty)
│   └── main.py
│
├── requirements.txt
└── start.sh
```

Purpose

- REST APIs
- AI pipeline execution
- File management
- Business logic

---

# API

```
api/

health.py

upload.py

pipeline.py

download.py

history.py

profile.py
```

Purpose

Defines all REST endpoints.

---

# Controllers

```
controllers/

upload_controller.py

pipeline_controller.py

download_controller.py

history_controller.py

profile_controller.py
```

Purpose

Receives API requests and invokes services.

---

# Services

```
services/

image_service.py

mesh_service.py

pointcloud_service.py

storage_service.py
```

Purpose

Contains business logic.

---

# Pipeline

```
pipeline/

run.py

image_pipeline.py

detection_pipeline.py

segmentation_pipeline.py

generation_pipeline.py

pointcloud_pipeline.py
```

Purpose

Coordinates complete AI workflow.

---

# AI Models

```
ai_models/

florence2/

grounding_dino/

sam2/

hunyuan3d/

rembg/

common/          (empty)
```

Purpose

Contains model wrappers.

No API logic should exist here.

---

# Florence-2

```
florence2/

loader.py

caption.py

part_detection.py
```

---

# GroundingDINO

```
grounding_dino/

loader.py

detector.py
```

---

# SAM2.1

```
sam2/

loader.py

segment.py
```

---

# Hunyuan3D-2

```
hunyuan3d/

loader.py

generator.py
```

---

# rembg

```
rembg/

background_removal.py
```

---

# Utilities

```
utils/

image_utils.py

mesh_utils.py

pointcloud_utils.py

validators.py

logger.py

artifacts_manager.py
```

Purpose

Reusable helper functions.

---

# Schemas

```
schemas/

upload_schema.py

response_schema.py

pipeline_schema.py
```

Purpose

Pydantic request/response models.

---

# Core

```
core/

settings.py

constants.py

exceptions.py

auth.py

database.py
```

Purpose

Application configuration and cross-cutting concerns (JWT auth, Supabase sync).

---

# Middleware

```
middleware/

exception_middleware.py
```

Purpose

Centralized error handling and consistent JSON error responses.

---

# Config Files

```
configs/

app.yaml

dbscan.yaml

florence2.yaml

frontend.yaml

grounding_dino.yaml

hunyuan3d.yaml

image_processing.yaml

logging.yaml

pointcloud.yaml

rembg.yaml

sam2.yaml
```

Purpose

Stores configurable parameters for each module.

---

# Frontend

```
frontend/

app/

components/

hooks/          (empty)

types/          (empty)

styles/

public/

context/

utils/
```

Purpose

User interface.

---

# Components

```
components/

Auth/
  LoginForm.tsx
  SignupForm.tsx
  ForgotPasswordForm.tsx
  ProtectedRoute.tsx

Download/
  DownloadPanel.tsx

Footer/
  Footer.tsx

History/
  HistoryGrid.tsx
  HistoryCard.tsx
  SearchBar.tsx
  SortMenu.tsx

Navbar/
  Navbar.tsx

Profile/
  ProfileCard.tsx
  StatisticsCard.tsx

Progress/
  ProgressTracker.tsx

ThreeViewer.tsx
```

Purpose

Reusable UI components.

---

# Pages

```
app/

page.tsx                     (Landing)

upload/page.tsx

viewer/page.tsx

download/page.tsx

processing/[jobId]/page.tsx

results/[jobId]/page.tsx

history/page.tsx

profile/page.tsx

login/page.tsx

signup/page.tsx

forgot-password/page.tsx
```

---

# Context & Utils

```
context/

AuthContext.tsx

utils/

supabaseClient.ts
```

Purpose

Frontend state management and Supabase client initialization.

---

# Data

```
data/

input/

processed/

temp/

cache/
```

Purpose

Stores uploaded and intermediate files.

---

# Outputs

```
outputs/

<job_id>/
  original.png
  result.json
  detection.png
  enhanced.png
  segmentation.png
  rgba.png
  caption.txt
  grounding_prompt.txt
  mask.png
  mask_overlay.png
  part_detection.png
  model.glb
  model.obj (optional)
  pointcloud.ply
  segmented_pointcloud.ply
  preview.png
  scene.json

  debug/
    (pipeline debug artifacts)
```

Purpose

Flat per-job output directory structure.

---

# Scripts

```
scripts/

setup_environment.py

build_report.py
```

Purpose

Automation scripts.

---

# Tests

```
tests/

unit/

integration/

performance/

fixtures/

e2e/

frontend/
```

Purpose

Automated testing.

Unit tests cover individual modules (caption, detection, segmentation, shape generation, texture generation, point cloud, dbscan, upload, download, health, auth, config, etc.).

Integration tests cover the full API flow.

Performance tests benchmark pipeline throughput.

Frontend tests use Playwright for UI testing.

---

# Documentation

```
docs/

01_PROJECT_OVERVIEW.md

02_REQUIREMENTS.md

03_TECH_STACK.md

04_SYSTEM_ARCHITECTURE.md

05_FOLDER_STRUCTURE.md

06_AI_MODELS.md

07_PIPELINE.md

08_BACKEND_API.md

09_FRONTEND.md

10_DATABASE.md

11_INSTALLATION.md

12_CONFIGURATION.md

13_TESTING.md

14_DEPLOYMENT.md

15_FUTURE_SCOPE.md
```

---

# Logs

```
logs/

backend.log

pipeline.log

errors.log
```

---

# Docker

```
docker/

(empty)
```

---

# Naming Convention

Python Files

snake_case.py

Example

```
pointcloud_generator.py
```

Python Classes

PascalCase

Example

```
PointCloudGenerator
```

Variables

snake_case

Example

```
generated_mesh
```

API Routes

kebab-case

Example

```
/generate-3d
```

Environment Variables

UPPER_CASE

Example

```
CUDA_DEVICE
MODEL_PATH
OUTPUT_PATH
```

---

# Architecture Rules

- Each AI model must be isolated.
- Controllers must never contain AI logic.
- Services must never contain API definitions.
- Utility functions must be reusable.
- Configuration values must not be hardcoded.
- Intermediate outputs must be stored in the `data/temp` directory.
- Final outputs must be stored only in the `outputs` directory.
- Each processing stage should log its execution to `logs/pipeline.log`.
- Model loading and unloading should be managed centrally to optimize GPU memory usage.

---

# Final Project Structure

```
single-image-3d-system/

backend/
frontend/
ai_models/
configs/
data/
outputs/
scripts/
tests/
docs/
logs/
docker/

README.md
requirements.txt
docker-compose.yml
LICENSE
```
