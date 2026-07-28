
# AI Processing Pipeline

## Overview

The AI Processing Pipeline is the core execution engine of the system. It transforms a single RGB image into a textured 3D asset (GLB) and a segmented point cloud (PLY) through a sequence of sequential stages, each unloading VRAM before the next stage loads.

The pipeline is triggered as a **background task** during image upload — there is no separate `/pipeline/start` endpoint.

Each stage:
- Validates its own output
- Logs start/end time, duration, status
- Syncs progress and artifacts to **Supabase** database

---

# Complete Workflow

```
User Upload (POST /api/v1/upload)
      │
      ▼
Image Validation
      │
      ▼
Image Analysis
      │
      ▼
CLAHE Enhancement (Conditional — based on brightness/contrast threshold)
      │
      ▼
Florence-2 Caption Generation
      │
      ▼
GroundingDINO Object Detection (multi-pass threshold retry)
      │
      ▼
Florence-2 Part Detection
      │
      ▼
SAM2.1 Instance Segmentation
      │
      ▼
Background Removal (rembg + ONNX)
      │
      ▼
Hunyuan3D-2 Shape Generation (progressive retry: GPU / lower-res / CPU)
      │
      ▼
Hunyuan3D-2 Texture Generation (progressive retry: GPU / lower-res / CPU)
      │
      ▼
Open3D Mesh Validation
      │
      ▼
Point Cloud Generation (Poisson Disk Sampling)
      │
      ▼
DBSCAN Point Cloud Segmentation
      │
      ▼
Export Results
```

---

# Status Values

Status (from `result.json` and `GET /pipeline/status/{job_id}`):

- `processing` — Job initialized, pipeline running
- `completed` — All stages finished
- `failed` — A stage raised an unrecoverable error
- `not_found` — Job directory does not exist

---

# Stage-by-Stage

## Stage 1 — Upload & Validation

- **Input**: JPG, JPEG, PNG, WEBP, BMP (max 25 MB)
- **Actions**: File type check, RGB conversion, image readability
- **Output**: `outputs/<job_id>/original.png`
- **DB Sync**: Creates `jobs` + `artifacts` rows in Supabase

## Stage 2 — Image Analysis

- Calculates: width, height, mean brightness, standard deviation
- Decision: brightness < threshold → CLAHE applied

## Stage 3 — CLAHE Enhancement

- Library: OpenCV
- Converts RGB → LAB → CLAHE → RGB
- Output: `outputs/<job_id>/enhanced.png`

## Stage 4 — Caption Generation

- Model: Florence-2
- Output: raw caption → transformed to dot-separated prompt (e.g. `black . ceramic . mug`)
- Artifacts: `caption.txt`, `grounding_prompt.txt`

## Stage 5 — Object Detection (GroundingDINO)

- Multi-pass threshold strategy (not fixed retry count):
  - Pass 1: threshold 0.20
  - Pass 2: threshold 0.20 (CLAHE image fallback)
  - Pass 3: threshold 0.15
  - Pass 4: threshold 0.10
- Output: bounding box, confidence score, label
- Artifact: `detection.png` (visual overlay)

## Stage 6 — Part Detection

- Model: Florence-2
- Candidate parts: body, handle, base, wheels, lid, seat, backrest, legs
- Output: part bounding boxes
- Artifact: `part_detection.png`

## Stage 7 — Segmentation

- Model: SAM2.1
- Input: image + part boxes
- Output: binary mask (highest IoU selected)
- Artifacts: `mask.png`, `segmentation.png` (mask overlay)

## Stage 8 — Background Removal

- Tool: rembg (ONNX Runtime)
- Output: RGBA PNG (`rgba.png`)
- Validation: alpha channel must exist

## Stage 9 — Shape Generation

- Model: Hunyuan3D-2
- Progressive retry:
  1. GPU with full config
  2. GPU with lower octree (96)
  3. GPU with minimum steps + low octree
  4. CPU fallback
- Output: `outputs/<job_id>/model.glb`
- Validation: vertices > 0, faces > 0

## Stage 10 — Texture Generation

- Model: Hunyuan3D-2
- Progressive retry:
  1. GPU at configured resolution
  2. GPU at 128px
  3. CPU at 128px
- Output: textured GLB (overwrites `outputs/<job_id>/model.glb`)

## Stage 11 — Mesh Validation

- Library: Open3D
- Checks: mesh loads, normals computed, no missing geometry

## Stage 12 — Point Cloud Generation

- Algorithm: Poisson Disk Sampling
- Target: 100,000 points
- Output: `outputs/pointcloud/<job_id>_pointcloud.ply` + copy in job dir

## Stage 13 — DBSCAN Segmentation

- Parameters: eps = 0.05, min_points = 50
- Output: `outputs/pointcloud/<job_id>_segmented_pointcloud.ply`
- Metadata: cluster count, outlier count

---

# Output Structure

```
outputs/
  <job_id>/
    original.png
    enhanced.png         (if CLAHE applied)
    detection.png
    segmentation.png
    mask_overlay.png
    part_detection.png
    rgba.png
    mask.png
    model.glb
    pointcloud.ply
    segmented_pointcloud.ply
    caption.txt
    grounding_prompt.txt
    result.json           (master metadata + artifacts map)
  meshes/
    <job_id>_model.glb
  pointcloud/
    <job_id>_pointcloud.ply
    <job_id>_segmented_pointcloud.ply
```

---

# Database Sync

Each stage syncs to Supabase:

- `jobs` table: status, duration, model/pointcloud generated flags
- `artifacts` table: artifact_type, storage_path, file_size, mime_type

Performed inside `artifacts_manager.py` methods (`add_file_artifact`, `add_text_artifact`, `update_status`).

---

# GPU Memory Strategy

Models are loaded one-at-a-time:

```
Load Florence-2 → Inference → Unload → Clear CUDA Cache
Load GroundingDINO → Inference → Unload → Clear CUDA Cache
Load SAM2.1 → Inference → Unload → Clear CUDA Cache
Load Hunyuan3D-2 Shape → Inference → Unload → Clear CUDA Cache
Load Hunyuan3D-2 Texture → Inference → Unload → Clear CUDA Cache
```

Prevents GPU OOM on consumer cards (4–8 GB VRAM).

---

# Pipeline Success Criteria

The execution is successful if all stages complete and produce:

- `detection.png`
- `segmentation.png`
- `rgba.png`
- `model.glb`
- `pointcloud.ply`
- `segmented_pointcloud.ply`
- `result.json`
