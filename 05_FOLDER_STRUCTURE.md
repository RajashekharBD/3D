
# Project Folder Structure

## Overview

This document defines the complete production-ready folder structure for the Automated Single-Image to 3D Asset and Point Cloud Generation System.

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
│   ├── models/
│   ├── utils/
│   ├── schemas/
│   ├── middleware/
│   ├── core/
│   ├── config/
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

upload.py

detect.py

segment.py

generate3d.py

pointcloud.py

download.py

health.py
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

pipeline_manager.py

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

common/
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

shape_generation.py

texture_generation.py

mesh_export.py
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

cuda_utils.py

logger.py

validators.py

file_utils.py
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
```

Purpose

Application configuration.

---

# Config

```
configs/

model_config.yaml

pipeline.yaml

dbscan.yaml

logging.yaml
```

Purpose

Stores configurable parameters.

---

# Frontend

```
frontend/

app/

components/

hooks/

services/

styles/

public/

types/

utils/
```

Purpose

User interface.

---

# Components

```
components/

Upload/

Viewer/

Progress/

Download/

Layout/

Navbar/

Footer/
```

Purpose

Reusable UI components.

---

# Pages

```
app/

page.tsx

upload/

viewer/

download/
```

---

# Services

```
services/

api.ts

upload.ts

download.ts
```

Purpose

Frontend API communication.

---

# Public

```
public/

icons/

images/

logo/

fonts/
```

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

images/

meshes/

pointcloud/

metadata/
```

---

# Images

```
images/

detection.png

segmentation.png

rgba.png
```

---

# Meshes

```
meshes/

model.glb
```

---

# Point Cloud

```
pointcloud/

pointcloud.ply

segmented_pointcloud.ply
```

---

# Metadata

```
metadata/

result.json

pipeline.json
```

---

# Scripts

```
scripts/

download_models.py

setup_environment.py

clean_outputs.py

benchmark.py
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
```

Purpose

Automated testing.

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

Dockerfile.backend

Dockerfile.frontend
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
