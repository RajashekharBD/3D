
# AI Processing Pipeline

## Overview

The AI Processing Pipeline is the core execution engine of the system. It transforms a single RGB image into a textured 3D asset (GLB) and a segmented point cloud (PLY) through a sequence of independent processing stages.

Each stage has:

- Defined input
- Processing logic
- Output
- Validation
- Error handling
- Retry mechanism

The pipeline is synchronous—each stage must complete successfully before the next begins.

---

# Complete Workflow

```
User Upload
      │
      ▼
Image Validation
      │
      ▼
Image Analysis
      │
      ▼
CLAHE Enhancement (Optional)
      │
      ▼
Florence-2 Caption Generation
      │
      ▼
GroundingDINO Object Detection
      │
      ▼
Florence-2 Part Detection
      │
      ▼
SAM2.1 Instance Segmentation
      │
      ▼
Background Removal
      │
      ▼
Hunyuan3D-2 Shape Generation
      │
      ▼
Hunyuan3D-2 Texture Generation
      │
      ▼
GLB Validation
      │
      ▼
Open3D Mesh Processing
      │
      ▼
Point Cloud Generation
      │
      ▼
Surface Normal Estimation
      │
      ▼
DBSCAN Segmentation
      │
      ▼
Export Results
```

---

# Stage 1 — Image Upload

## Input

- JPG
- JPEG
- PNG
- WEBP
- BMP

## Validation

Check:

- File exists
- Valid extension
- Readable image
- RGB conversion

## Output

```
RGB Image
```

---

# Stage 2 — Image Analysis

Calculate:

- Width
- Height
- Channels
- Mean Brightness
- Standard Deviation

Decision:

```
Brightness < Threshold ?

YES

↓

Apply CLAHE

NO

↓

Continue
```

---

# Stage 3 — CLAHE Enhancement

Library

OpenCV

Processing

RGB

↓

LAB Color Space

↓

CLAHE

↓

RGB

Output

Enhanced Image

---

# Stage 4 — Caption Generation

Model

Florence-2

Input

Enhanced Image

Output

```
"a black ceramic mug"
```

Validation

Caption must not be empty.

---

# Stage 5 — Prompt Generation

Convert

```
a black ceramic mug
```

into

```
black . ceramic . mug
```

Output

GroundingDINO Prompt

---

# Stage 6 — Object Detection

Model

GroundingDINO

Input

Image

Prompt

Output

Bounding Boxes

Confidence

Labels

---

Detection Strategy

```
Pass 1

Original Image

Threshold 0.20

↓

If Failed

↓

Pass 2

CLAHE Image

↓

If Failed

↓

Threshold 0.15

↓

If Failed

↓

Threshold 0.10

↓

If Failed

↓

Pipeline Stops
```

---

# Stage 7 — Part Detection

Model

Florence-2

Input

Detected Object

Output

Example

```
Body

Handle
```

Output

Part Bounding Boxes

---

# Stage 8 — Segmentation

Model

SAM2.1

Input

Image

Part Boxes

Output

Binary Masks

Mask Scores

IoU Scores

Decision

Highest IoU

↓

Final Mask

---

# Stage 9 — Background Removal

Tool

rembg

Backend

ONNX Runtime

Input

Mask

Image

Output

RGBA Image

Transparent Background

Validation

Alpha channel must exist.

---

# Stage 10 — Shape Generation

Model

Hunyuan3D-2

Input

RGBA Image

Output

Watertight Mesh

Validation

Mesh contains:

- Vertices
- Faces

---

# Stage 11 — Texture Generation

Model

Hunyuan3D-2

Input

Mesh

RGBA

Output

Textured GLB

Validation

Texture exists

GLB readable

---

# Stage 12 — Mesh Validation

Library

Open3D

Checks

Mesh loads

Normals computed

No missing geometry

Output

Validated Mesh

---

# Stage 13 — Point Cloud Generation

Algorithm

Poisson Disk Sampling

Input

GLB

Output

PLY

Target

100000 Points

Validation

Point Count

Normals

---

# Stage 14 — Surface Normals

Compute

Normals

↓

Orient Normals

↓

Save

---

# Stage 15 — Point Cloud Segmentation

Algorithm

DBSCAN

Input

PLY

Parameters

```
eps = 0.05

min_points = 50
```

Output

Colored Clusters

---

# Stage 16 — Export

Generate

```
outputs/

images/

detection.png

segmentation.png

rgba.png

meshes/

model.glb

pointcloud/

pointcloud.ply

segmented_pointcloud.ply

metadata/

result.json
```

---

# Validation Pipeline

Each stage validates its own output before continuing.

```
Stage Success ?

YES

↓

Next Stage

NO

↓

Retry

↓

Still Failed

↓

Stop Pipeline
```

---

# Retry Logic

## Detection

Retry Count

4

---

## Segmentation

Retry Count

1

---

## Background Removal

Retry Count

1

---

## Hunyuan3D

Retry Count

1

---

## Open3D

Retry Count

1

---

# GPU Memory Strategy

```
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

Load Hunyuan3D

↓

Inference

↓

Unload

↓

Clear CUDA Cache
```

This prevents GPU memory exhaustion.

---

# Logging

Every stage logs:

- Start Time
- End Time
- Duration
- Status
- Errors
- Output File

Example

```
Stage: Detection

Status: Success

Time: 4.1 Seconds

Confidence: 0.34
```

---

# Final Outputs

Images

- Detection Image
- Segmentation Image
- RGBA Image

3D

- GLB Mesh

Point Cloud

- Raw PLY
- Segmented PLY

Metadata

- JSON Report

---

# Pipeline Success Criteria

The execution is successful only if all stages complete and the following files are produced:

✓ detection.png

✓ segmentation.png

✓ rgba.png

✓ model.glb

✓ pointcloud.ply

✓ segmented_pointcloud.ply

✓ result.json
