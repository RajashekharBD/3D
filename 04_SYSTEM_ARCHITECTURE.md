
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

↓

Mesh Viewer

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

# Frontend Architecture

User

↓

Next.js

↓

React Components

↓

Upload Page

↓

Progress Page

↓

Viewer Page

↓

Download Page

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

# Error Handling Flow

Upload Error

↓

Validate Image

↓

Retry

↓

Abort

---

Detection Failure

↓

Retry Detection

↓

Lower Threshold

↓

Enhanced Image

↓

Abort

---

Segmentation Failure

↓

Retry SAM2

↓

Abort

---

3D Failure

↓

Retry Generation

↓

Abort

---

Point Cloud Failure

↓

Regenerate Mesh

↓

Retry

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

This sequential loading minimizes GPU memory usage and enables execution on GPUs with limited VRAM.

---

# Output Files

outputs/

images/

- detection.png
- segmentation.png
- rgba.png

meshes/

- model.glb

pointcloud/

- pointcloud.ply
- segmented_pointcloud.ply

metadata/

- result.json

logs/

- pipeline.log

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
