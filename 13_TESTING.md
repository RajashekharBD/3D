
# Testing Strategy

## Overview

This document defines the testing strategy for the Automated Single-Image to 3D Asset and Point Cloud Generation System.

The objectives are to:

- Verify correctness
- Ensure robustness
- Validate AI pipeline outputs
- Measure performance
- Detect regressions
- Ensure production readiness

---

# Testing Levels

The project uses five levels of testing.

```
Unit Testing

↓

Integration Testing

↓

System Testing

↓

Performance Testing

↓

Acceptance Testing
```

---

# Testing Environment

Operating System

Windows 11

Python

3.11+

GPU

NVIDIA RTX 3050

RAM

16 GB

CUDA

12.1

---

# Unit Testing

## Goal

Verify every module independently.

Modules

- Image Validation
- Image Enhancement
- Florence-2
- GroundingDINO
- SAM2.1
- rembg
- Hunyuan3D-2
- Open3D
- DBSCAN

---

## UT-01

Image Validation

Input

Valid JPG

Expected

Accepted

Status

PASS

---

## UT-02

Unsupported Format

Input

PDF

Expected

Rejected

PASS

---

## UT-03

Brightness Detection

Input

Dark Image

Expected

Brightness < 0.30

PASS

---

## UT-04

CLAHE

Input

Dark Image

Expected

Enhanced Image Generated

PASS

---

## UT-05

Florence-2 Caption

Expected

Caption not empty

PASS

---

## UT-06

GroundingDINO

Expected

Bounding Box Generated

PASS

---

## UT-07

SAM2.1

Expected

Binary Mask Generated

PASS

---

## UT-08

Background Removal

Expected

Transparent RGBA Image

PASS

---

## UT-09

Hunyuan3D-2

Expected

GLB Generated

PASS

---

## UT-10

Open3D

Expected

Mesh Loaded Successfully

PASS

---

## UT-11

Point Cloud

Expected

PLY Generated

PASS

---

## UT-12

DBSCAN

Expected

Clusters Generated

PASS

---

# Integration Testing

## Goal

Verify interaction between modules.

---

## IT-01

Florence-2

↓

GroundingDINO

Expected

Caption correctly converted into detection prompt.

---

## IT-02

GroundingDINO

↓

SAM2.1

Expected

Bounding boxes correctly segmented.

---

## IT-03

SAM2.1

↓

rembg

Expected

RGBA image generated.

---

## IT-04

rembg

↓

Hunyuan3D-2

Expected

3D model generated.

---

## IT-05

Hunyuan3D-2

↓

Open3D

Expected

Mesh loads successfully.

---

## IT-06

Open3D

↓

DBSCAN

Expected

Point cloud segmented successfully.

---

# System Testing

Entire pipeline.

Input

One RGB Image

Expected

All outputs generated.

Outputs

✓ Detection Image

✓ Segmentation Image

✓ RGBA Image

✓ GLB

✓ Point Cloud

✓ Segmented Point Cloud

✓ Metadata

---

# Performance Testing

Measure execution time.

---

Image Validation

Target

< 1 sec

---

CLAHE

Target

< 2 sec

---

Florence-2

Target

< 5 sec

---

GroundingDINO

Target

< 6 sec

---

SAM2.1

Target

< 6 sec

---

Background Removal

Target

< 3 sec

---

Hunyuan3D Shape

Target

< 180 sec

---

Texture Generation

Target

< 90 sec

---

Point Cloud

Target

< 10 sec

---

DBSCAN

Target

< 5 sec

---

Total Pipeline

Target

≤ 4 Minutes

---

# GPU Testing

Verify

- CUDA Available
- GPU Memory Usage
- GPU Temperature (optional)
- Model Loading
- Model Unloading

Expected

No CUDA Out Of Memory Error

---

# Memory Testing

Measure

RAM

VRAM

Temporary Files

Expected

No Memory Leak

---

# Stress Testing

Repeated Runs

10 Images

Expected

Stable Execution

---

Large Image

6000×4000

Expected

Graceful Processing or Validation Error

---

Invalid Image

Expected

Proper Error Message

---

# Error Handling Tests

Corrupted Image

↓

Rejected

PASS

---

Unsupported Extension

↓

Rejected

PASS

---

Missing Model

↓

Error Logged

PASS

---

GPU Not Available

↓

Fallback or Clear Error

PASS

---

Disk Full

↓

Graceful Failure

PASS

---

# Output Validation

Detection Image

Bounding Box Visible

PASS

---

Segmentation Image

Mask Correct

PASS

---

RGBA Image

Transparent Background

PASS

---

GLB

Loads in Open3D

PASS

---

Point Cloud

Correct Point Count

PASS

---

DBSCAN

Clusters Generated

PASS

---

# Acceptance Criteria

The system is accepted if:

✓ Valid image uploads succeed.

✓ Unsupported files are rejected.

✓ Caption generation succeeds.

✓ Object detection succeeds.

✓ Segmentation succeeds.

✓ Background removal succeeds.

✓ GLB generation succeeds.

✓ Point cloud generation succeeds.

✓ Point cloud segmentation succeeds.

✓ All outputs are downloadable.

✓ Total execution time meets target.

---

# Automated Testing

Recommended Tools

Backend

pytest

Frontend

Playwright

API

pytest + FastAPI TestClient

Coverage

pytest-cov

Static Analysis

ruff

Formatting

black

Type Checking

mypy

---

# Regression Testing

Run after every major change.

Verify

- Upload
- Pipeline
- Outputs
- Downloads
- API Responses

---

# Test Report

Each execution stores:

- Job ID
- Test Date
- Environment
- GPU
- Execution Time
- Result
- Errors (if any)

---

# Exit Criteria

The project is considered production-ready when:

- All unit tests pass
- All integration tests pass
- All system tests pass
- No critical defects remain
- Pipeline completes successfully
- Performance targets are met
- Outputs are validated
