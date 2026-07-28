
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

# Automated Tests

## Backend (pytest)

| Suite | Files | Tests | Status |
|---|---|---|---|
| Unit (`tests/unit/`) | 20 | 53 | All PASS |
| Integration (`tests/integration/test_e2e_api.py`) | 1 | 30 | All PASS |
| Performance (`tests/performance/test_benchmarks.py`) | 1 | 10 | All PASS |
| **Total Backend** | **22** | **93** | **All PASS** |

### Unit Test Files (20)

| File | Stage |
|---|---|
| `test_upload.py` | Upload |
| `test_validation.py` | Validation |
| `test_analysis.py` | Image Analysis |
| `test_clahe.py` | CLAHE Enhancement |
| `test_caption.py` | Florence-2 Captioning |
| `test_detection.py` | GroundingDINO Detection |
| `test_part_detection.py` | Florence-2 Part Detection |
| `test_segmentation.py` | SAM2.1 Segmentation |
| `test_background_removal.py` | Background Removal |
| `test_shape_generation.py` | Shape Generation |
| `test_texture_generation.py` | Texture Generation |
| `test_mesh_validation.py` | Mesh Validation |
| `test_pointcloud.py` | Point Cloud Generation |
| `test_dbscan.py` | DBSCAN Segmentation |
| `test_pipeline_status.py` | Pipeline Status API |
| `test_download.py` | Download API |
| `test_health.py` | Health API |
| `test_config.py` | Config Loading |
| `test_artifacts_manager.py` | Artifacts Manager |
| `test_auth_history.py` | Auth & History |

## Frontend (Playwright)

| File | Purpose |
|---|---|
| `tests/frontend/landing.spec.ts` | Landing page |
| `tests/frontend/upload.spec.ts` | Upload page |
| `tests/frontend/processing.spec.ts` | Processing page |
| `tests/frontend/results.spec.ts` | Results page |
| `tests/frontend/navigation.spec.ts` | Navigation & responsive |
| `tests/e2e/app.spec.ts` | End-to-end flow |

---

# Performance Targets

| Stage | Target | Actual (CI) | Status |
|---|---|---|---|
| Health API | < 1.0s | 0.008s | PASS |
| Upload + Validation | < 5.0s | 0.017s | PASS |
| Pipeline Status API | < 0.5s | 0.008s | PASS |
| Download List API | < 0.5s | 0.008s | PASS |
| Download Artifact API | < 0.5s | 0.009s | PASS |

---

# Coverage

- **Backend coverage:** 84% (measured via pytest-cov)
- Coverage data stored in `.coverage` (SQLite format)

---

# Test Report

The auto-generated test report is at `tests/report.md`. It includes:

- GPU information and memory usage
- API response time benchmarks
- Performance target compliance
- Full test suite summary
- Pipeline stage coverage matrix

---

# Automated Testing Tools

| Layer | Tool |
|---|---|
| Backend | pytest + FastAPI TestClient |
| Frontend | Playwright |
| Coverage | pytest-cov |
| Static Analysis | ruff |
| Formatting | black |
| Type Checking | mypy |

---

# Regression Testing

Run after every major change covering:

- Upload
- Pipeline
- Outputs
- Downloads
- API Responses

---

# Exit Criteria

The project is considered production-ready when:

- All unit tests pass
- All integration tests pass
- No critical defects remain
- Pipeline completes successfully
- Performance targets are met
- All outputs are validated
