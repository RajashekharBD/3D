
# Configuration Guide

## Overview

This document defines all configurable settings used by the Automated Single-Image to 3D Asset and Point Cloud Generation System.

The objective is to keep all configurable values outside the source code, making the application easier to maintain, deploy, and customize.

---

# Configuration Files

The project uses the following configuration files:

```
configs/

├── app.yaml
├── image_processing.yaml
├── florence2.yaml
├── grounding_dino.yaml
├── sam2.yaml
├── rembg.yaml
├── hunyuan3d.yaml
├── pointcloud.yaml
├── dbscan.yaml
├── logging.yaml
└── frontend.yaml
```

---

# Environment Variables

Create a `.env` file in the project root.

Example

```env
APP_NAME=SingleImage3D

APP_ENV=development

HOST=0.0.0.0

PORT=8000

LOG_LEVEL=INFO

CUDA_DEVICE=0

OUTPUT_DIR=outputs

TEMP_DIR=data/temp

MAX_UPLOAD_SIZE_MB=25

DELETE_TEMP_FILES=true

SUPABASE_URL=https://your-project.supabase.co

SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

SUPABASE_JWT_SECRET=your-jwt-secret
```

---

# Application Configuration

File

```
configs/app.yaml
```

```yaml
application:
  name: Single Image 3D System
  version: 1.0.0
  debug: true
  max_upload_size_mb: 25
  allowed_extensions:
    - jpg
    - jpeg
    - png
    - webp
    - bmp
```

---

# Image Processing Configuration

File

```
configs/image_processing.yaml
```

```yaml
image:
  brightness_threshold: 0.30
  contrast_threshold: 0.15
  apply_clahe: true

clahe:
  clip_limit: 2.0
  tile_grid_size: 8
```

---

# Florence-2 Configuration

File

```
configs/florence2.yaml
```

```yaml
florence2:
  device: cuda
  precision: float16
  max_tokens: 64
  temperature: 0.0
  beam_search: true
```

---

# GroundingDINO Configuration

File

```
configs/grounding_dino.yaml
```

```yaml
grounding_dino:
  thresholds:
    pass1: 0.20
    pass2: 0.20
    pass3: 0.15
    pass4: 0.10
  max_retries: 4
```

---

# SAM2.1 Configuration

File

```
configs/sam2.yaml
```

```yaml
sam2:
  multimask_output: true
  choose_best_iou: true
  device: cuda
```

---

# Background Removal

File

```
configs/rembg.yaml
```

```yaml
rembg:
  use_gpu: true
  output_format: RGBA
```

---

# Hunyuan3D-2 Configuration

File

```
configs/hunyuan3d.yaml
```

```yaml
hunyuan3d:
  shape_steps: 30
  guidance_scale: 5.5
  texture_steps: 10
  texture_resolution: 512
  export_format: glb
  octree_resolution: 256
  use_fp16: true
  cpu_offload: true
  sequential_cpu_offload: true
  attention_slicing: true
  vae_slicing: true
  vae_tiling: true
  lazy_loading: true
  retry_on_oom: true
```

---

# Point Cloud Configuration

File

```
configs/pointcloud.yaml
```

```yaml
pointcloud:
  target_points: 100000
  estimate_normals: true
  radius: 0.05
  max_neighbors: 30
  orient_normals: true
```

---

# DBSCAN Configuration

File

```
configs/dbscan.yaml
```

```yaml
dbscan:
  eps: 0.05
  min_points: 50
  remove_outliers: true
```

---

# Logging Configuration

File

```
configs/logging.yaml
```

```yaml
logging:
  level: INFO
  file: logs/pipeline.log
  console: true
  save_errors: true
```

---

# Frontend Configuration

File

```
configs/frontend.yaml
```

```yaml
frontend:
  polling_interval: 2000
  max_preview_size: 1200
  enable_dark_mode: false
```

---

# Output Directories

```
outputs/

images/

meshes/

pointcloud/

metadata/
```

These directories are automatically created if they do not exist.

---

# Runtime Configuration

The application loads configuration in the following order:

1. Default values
2. YAML configuration files
3. Environment variables
4. Runtime overrides

Later values override earlier ones.

---

# Validation Rules

At startup, the application validates:

- Required configuration files exist
- `.env` is present
- Output directories are writable
- CUDA availability (if enabled)
- Required model paths
- Disk space availability

If validation fails, the application exits with an error.

---

# Configuration Best Practices

- Do not hardcode configurable values in source code.
- Keep secrets only in `.env`.
- Use YAML files for model and pipeline parameters.
- Validate configuration before starting the pipeline.
- Keep development and production configurations separate.

---

# Configuration Summary

| Configuration         | Purpose                  |
| --------------------- | ------------------------ |
| app.yaml              | Application settings     |
| image_processing.yaml | Image enhancement        |
| florence2.yaml        | Caption generation       |
| grounding_dino.yaml   | Object detection         |
| sam2.yaml             | Segmentation             |
| rembg.yaml            | Background removal       |
| hunyuan3d.yaml        | 3D generation            |
| pointcloud.yaml       | Point cloud generation   |
| dbscan.yaml           | Point cloud segmentation |
| logging.yaml          | Logging                  |
| frontend.yaml         | Frontend behavior        |

The application is fully configurable without modifying the source code.
