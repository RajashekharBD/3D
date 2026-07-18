# Test & Performance Report

**Generated:** 2026-07-17 10:30:42
**Platform:** Windows 11
**Python:** 3.12.10
**CPU:** Intel64 Family 6 Model 154 Stepping 3, GenuineIntel (20 cores)
**RAM:** 15.7 GB total, 2.7 GB available
**CPU Load:** 19.2%

## GPU Information

- CUDA not available in this environment.

## Memory Usage

- **Baseline RSS:** 580.4 MB
- **Peak RSS:** 580.4 MB
- **Delta:** 0.0 MB

## API Response Times

| Stage | Time (sec) | Status |
|---|---|---|
| Health API | 0.0080 | OK |
| Upload + Validation | 0.0169 | OK |
| Pipeline Status API | 0.0084 | OK |
| Download List API | 0.0082 | OK |
| Download Artifact API | 0.0093 | OK |
| Upload Reject Large | 0.1163 | OK |
| Upload Reject Invalid | 0.0086 | OK |
| 3 Sequential Uploads (total) | 0.0575 | OK |

## Performance Targets

| Stage | Target | Actual | Status |
|---|---|---|---|
| Health API | < 1.0s | 0.0080s | PASS |
| Upload + Validation | < 5.0s | 0.0169s | PASS |
| Pipeline Status API | < 0.5s | 0.0084s | PASS |
| Download List API | < 0.5s | 0.0082s | PASS |
| Download Artifact API | < 0.5s | 0.0093s | PASS |

## Test Suite Summary

### Unit Tests

Total test files: **19**

- `test_analysis.py` - analysis
- `test_artifacts_manager.py` - artifacts_manager
- `test_background_removal.py` - background_removal
- `test_caption.py` - caption
- `test_clahe.py` - clahe
- `test_config.py` - config
- `test_dbscan.py` - dbscan
- `test_detection.py` - detection
- `test_download.py` - download
- `test_health.py` - health
- `test_mesh_validation.py` - mesh_validation
- `test_part_detection.py` - part_detection
- `test_pipeline_status.py` - pipeline_status
- `test_pointcloud.py` - pointcloud
- `test_segmentation.py` - segmentation
- `test_shape_generation.py` - shape_generation
- `test_texture_generation.py` - texture_generation
- `test_upload.py` - upload
- `test_validation.py` - validation

### Integration Tests

Total test files: **1**

- `test_e2e_api.py`

### Frontend Tests (Playwright)

Total test files: **5**

- `landing.spec.ts` - Landing page
- `upload.spec.ts` - Upload page
- `processing.spec.ts` - Processing page
- `results.spec.ts` - Results page
- `navigation.spec.ts` - Navigation & responsive

## Pipeline Stage Coverage

| Pipeline Stage | Test File | Status |
|---|---|---|
| Upload | `test_upload.py` | Covered |
| Validation | `test_validation.py` | Covered |
| Image Analysis | `test_analysis.py` | Covered |
| CLAHE Enhancement | `test_clahe.py` | Covered |
| Florence-2 Captioning | `test_caption.py` | Covered |
| GroundingDINO Detection | `test_detection.py` | Covered |
| Florence-2 Part Detection | `test_part_detection.py` | Covered |
| SAM2.1 Segmentation | `test_segmentation.py` | Covered |
| Background Removal | `test_background_removal.py` | Covered |
| Shape Generation | `test_shape_generation.py` | Covered |
| Texture Generation | `test_texture_generation.py` | Covered |
| Mesh Validation | `test_mesh_validation.py` | Covered |
| Point Cloud Generation | `test_pointcloud.py` | Covered |
| DBSCAN Segmentation | `test_dbscan.py` | Covered |
| Pipeline Status API | `test_pipeline_status.py` | Covered |
| Download API | `test_download.py` | Covered |

## Recommendations

1. **Full GPU Pipeline Benchmark**: Run the complete pipeline on a CUDA-enabled machine to measure AI model inference times.
2. **Load Testing**: Stress test concurrent uploads to measure API throughput.
3. **VRAM Monitoring**: Profile GPU memory during consecutive job runs to detect leaks.
4. **Browser Testing**: Expand Playwright tests to cover 3D viewer interactions and fullscreen mode.
