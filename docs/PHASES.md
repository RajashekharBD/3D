# Implementation Phases Tracker

This document serves as the single source of truth for tracking the implementation progress of the Automated Single-Image to 3D Asset and Point Cloud Generation System.

---

# Phase 1: Project Setup

**Status:** 🟩 Completed

**Completion Date:** 2026-07-16

**Objective:** Set up the root project directory, version control, python environment, backend/frontend directories, and project-level files.

**Modules Included:**
- Root directory configuration
- Scripts directory init

**Tasks:**
- Create root folder structure and initialize git repository
- Create `.gitignore`, `.env.example`, `docker-compose.yml`, `requirements.txt`, `README.md`, and `LICENSE` in the root
- Create `scripts/` directory with starter automation scripts (`setup_environment.py`)
- Setup virtual environment `.venv` and verify python version 3.11+

**Deliverables:**
- Root folder structure initialized
- Git repository configured
- Virtual environment created and activated
- Root configuration and setup files created

**Dependencies:** None

**Estimated Complexity:** Low

**Definition of Done:**
- [x] Root folder structure matches `05_FOLDER_STRUCTURE.md`
- [x] `.venv` is successfully created and python 3.11+ is active
- [x] Root documentation and git tracking initialized

**Files Created:**
- `.gitignore`
- `.env.example`
- `docker-compose.yml`
- `requirements.txt`
- `README.md`
- `LICENSE`
- `scripts/setup_environment.py`
- `data/input/.gitkeep` (and folder keeper files)

**Files Modified:** None

**Summary:** Set up the core project folder structure, configuration settings, environment properties template, requirements specification list, git repository tracking, and automatic workspace creation scripts.

**Known Issues:** None

**Tests Executed:** `python scripts/setup_environment.py` to create the directories and check versioning, and `.venv\Scripts\python --version` to check the virtual environment Python interpreter.

**Result:** Pass (successfully created all required folder layout and verified Python 3.12.10 virtual environment).

**Next Phase:** Phase 2: Backend Initialization

---

# Phase 2: Backend Initialization

**Status:** 🟩 Completed

**Completion Date:** 2026-07-16

**Objective:** Initialize the FastAPI backend application structure with default router, ASGI server, and basic setup.

**Modules Included:**
- `backend/`
- `backend/app/main.py`
- `backend/app/core/`

**Tasks:**
- Create `backend/requirements.txt` and `backend/start.sh`
- Create `backend/app` subfolder structure (`api/`, `controllers/`, `services/`, `pipeline/`, `models/`, `utils/`, `schemas/`, `middleware/`, `core/`, `config/`)
- Implement `backend/app/main.py` with FastAPI initialization and Uvicorn launch
- Implement `backend/app/core/settings.py` and `backend/app/core/constants.py`
- Implement basic exception handling middleware in `backend/app/middleware/` and `backend/app/core/exceptions.py`
- Implement a health check API endpoint at `/api/v1/health`

**Deliverables:**
- Backend API initialized with routing structure
- Health check endpoint returning `{"status": "healthy"}`
- `start.sh` and environment setup completed for the backend

**Dependencies:** Phase 1

**Estimated Complexity:** Low

**Definition of Done:**
- [x] Backend runs via Uvicorn on port 8000
- [x] `GET /api/v1/health` returns status `healthy`
- [x] No linting or runtime errors on startup

**Files Created:**
- `backend/requirements.txt`
- `backend/start.sh`
- `backend/app/main.py`
- `backend/app/core/settings.py`
- `backend/app/core/constants.py`
- `backend/app/core/exceptions.py`
- `backend/app/middleware/exception_middleware.py`
- `backend/app/api/health.py`
- `tests/unit/test_health.py`

**Files Modified:** None

**Summary:** Initialized the backend FastAPI application directory structure, set up core configuration models, created exception models and error-formatting middleware, and implemented the `/api/v1/health` status endpoint.

**Known Issues:** None

**Tests Executed:** `pytest tests/unit/test_health.py`

**Result:** Pass (health endpoint returned status code 200 with status "healthy").

**Next Phase:** Phase 3: Frontend Initialization

---

# Phase 3: Frontend Initialization

**Status:** 🟩 Completed

**Completion Date:** 2026-07-16

**Objective:** Initialize the Next.js 15 frontend application with React 19, TypeScript, and Tailwind CSS.

**Modules Included:**
- `frontend/`

**Tasks:**
- Initialize Next.js 15 in the `frontend/` directory
- Configure TypeScript, Tailwind CSS, and layout skeleton
- Create directory structure (`frontend/app/`, `frontend/components/`, `frontend/hooks/`, `frontend/services/`, `frontend/types/`, `frontend/utils/`, `frontend/public/`)
- Set up core routing paths (`/`, `/upload`, `/processing/[jobId]`, `/results/[jobId]`)
- Create shared layout components: `Navbar` and `Footer`

**Deliverables:**
- Next.js frontend project skeleton running
- Basic layout (Navbar, Footer, Main container) configured
- Pages set up with placeholder screens

**Dependencies:** Phase 1

**Estimated Complexity:** Low

**Definition of Done:**
- [x] Next.js app builds and runs successfully on port 3000
- [x] Home landing page displays correctly in the browser
- [x] No compilation or console errors

**Files Created:**
- `frontend/*` (Next.js app project structure)
- `frontend/components/Navbar/Navbar.tsx`
- `frontend/components/Footer/Footer.tsx`
- `frontend/app/upload/page.tsx`
- `frontend/app/processing/[jobId]/page.tsx`
- `frontend/app/results/[jobId]/page.tsx`
- `frontend/app/viewer/page.tsx`
- `frontend/app/download/page.tsx`

**Files Modified:**
- `frontend/app/layout.tsx`
- `frontend/app/page.tsx`

**Summary:** Initialized the Next.js 15 app structure with Tailwind CSS, TypeScript, and ESLint. Set up core layouts (Navbar, Footer), customized metadata titles, configured pages for uploads, processing states, viewer visualization interfaces, and verified compile compliance.

**Known Issues:** None

**Tests Executed:** `npm run build` inside `./frontend`

**Result:** Pass (the Next.js project compiled cleanly to production assets with zero errors).

**Next Phase:** Phase 4: Configuration

---

# Phase 4: Configuration

**Status:** 🟩 Completed

**Completion Date:** 2026-07-16

**Objective:** Implement externalized YAML and environment configuration loaders in the backend.

**Modules Included:**
- `configs/`
- `backend/app/core/settings.py`

**Tasks:**
- Create YAML configuration files in `configs/` (`app.yaml`, `image_processing.yaml`, `florence2.yaml`, `grounding_dino.yaml`, `sam2.yaml`, `rembg.yaml`, `hunyuan3d.yaml`, `pointcloud.yaml`, `dbscan.yaml`, `logging.yaml`, `frontend.yaml`)
- Implement a configuration loader service in `backend/app/core/settings.py` using PyYAML/Pydantic Settings
- Bind `.env` variable overrides to settings
- Create `backend/app/utils/logger.py` matching logging config and write startup logs to `logs/backend.log`

**Deliverables:**
- YAML configurations successfully parsed and validated on backend startup
- Logger initialization logging to console and `logs/backend.log`
- Configuration validation mechanism at application boot

**Dependencies:** Phase 2

**Estimated Complexity:** Medium

**Definition of Done:**
- [x] Settings load all values from YAML and override using `.env`
- [x] Invalid configs cause backend to fail fast with descriptive error logs
- [x] Logging generates log files under `logs/` directory

**Files Created:**
- `configs/app.yaml`
- `configs/image_processing.yaml`
- `configs/florence2.yaml`
- `configs/grounding_dino.yaml`
- `configs/sam2.yaml`
- `configs/rembg.yaml`
- `configs/hunyuan3d.yaml`
- `configs/pointcloud.yaml`
- `configs/dbscan.yaml`
- `configs/logging.yaml`
- `configs/frontend.yaml`
- `backend/app/utils/logger.py`
- `tests/unit/test_config.py`

**Files Modified:**
- `backend/app/core/settings.py`

**Summary:** Implemented externalized YAML configuration files under `configs/`, refactored `backend/app/core/settings.py` to dynamically load, validate, and bind them with environment overrides using Pydantic, and initialized standard logging to `logs/pipeline.log`.

**Known Issues:** None

**Tests Executed:** `pytest tests/unit/test_config.py`

**Result:** Pass (all configurations loaded successfully with exact type matching, and logger writes outputs without throwing errors).

**Next Phase:** Phase 5: Image Upload

---

# Phase 5: Image Upload

**Status:** 🟩 Completed

**Completion Date:** 2026-07-16

**Objective:** Implement file upload endpoint, validation, local storage logic, and UUID job creation.

**Modules Included:**
- `backend/app/api/upload.py`
- `backend/app/controllers/upload_controller.py`
- `backend/app/services/storage_service.py`
- `backend/app/schemas/upload_schema.py`
- `frontend/components/Upload/`
- `frontend/app/upload/`

**Tasks:**
- Create directories `data/input`, `data/processed`, `data/temp`
- Create `POST /api/v1/upload` endpoint returning a unique `job_id`
- Implement file size and format validation in backend services
- Implement the Frontend Drag-and-Drop / File Picker component in `frontend/components/Upload/`
- Connect frontend upload form to the `/api/v1/upload` backend endpoint and transition to `/processing/[jobId]` upon receipt of `job_id`

**Deliverables:**
- Backend API processing image uploads and saving them to `data/input/`
- Unique job ID generated and returned for each valid upload
- Interactive drag-and-drop frontend component communicating with backend upload route

**Dependencies:** Phase 2, Phase 3, Phase 4

**Estimated Complexity:** Medium

**Definition of Done:**
- [x] File uploads under 25MB save successfully to `data/input/<job_id>_original.<ext>`
- [x] Uploading file >25MB or invalid formats returns HTTP 400
- [x] Frontend successfully redirects to `/processing/[jobId]` after upload

**Files Created:**
- `backend/app/schemas/response_schema.py`
- `backend/app/schemas/upload_schema.py`
- `backend/app/services/storage_service.py`
- `backend/app/controllers/upload_controller.py`
- `backend/app/api/upload.py`
- `tests/unit/test_upload.py`

**Files Modified:**
- `backend/app/main.py`
- `frontend/app/upload/page.tsx`

**Summary:** Created directories (`data/input/`, `outputs/images/`, etc.), set up the POST `/api/v1/upload` route validating image size (<25MB) and extension types, and implemented a drag-and-drop frontend UI with previews and API redirection.

**Known Issues:** None

**Tests Executed:** `pytest tests/unit/test_upload.py` and `npm run build` inside `./frontend`

**Result:** Pass (all tests successfully passed and frontend compiled without errors).

**Next Phase:** Phase 6: Image Validation

---

# Phase 6: Image Validation

**Status:** ⬜ Not Started

**Objective:** Implement strict programmatic validation of the uploaded image file in the backend service.

**Modules Included:**
- `backend/app/utils/validators.py`
- `backend/app/services/image_service.py`

**Tasks:**
- Implement detailed file header check (magic byte validation) to reject renamed malicious files
- Verify image readability using Pillow (try opening and verifying integrity)
- Implement exception classes for image corruption and format violations

**Deliverables:**
- Robust image validation helper utility
- Automated rejection of corrupted or disguised image files

**Dependencies:** Phase 5

**Estimated Complexity:** Low

**Definition of Done:**
- [ ] Magic byte verification correctly identifies and rejects corrupted or disguised binaries
- [ ] Correctly formatted images pass validation without overhead

---

# Phase 7: Image Processing (Analysis)

**Status:** ⬜ Not Started

**Objective:** Implement initial image analysis stage to calculate properties and determine if CLAHE enhancement is needed.

**Modules Included:**
- `backend/app/utils/image_utils.py`
- `backend/app/services/image_service.py`

**Tasks:**
- Implement OpenCV resolution, color channel, mean brightness, and contrast extraction
- Write logic to check if mean brightness is below threshold (default 0.30) or contrast is below threshold (default 0.15)
- Store calculated metrics in job metadata report (`outputs/metadata/<job_id>_result.json`)

**Deliverables:**
- Image properties analyzer module
- Dynamic flag determination for enhancement pipeline step

**Dependencies:** Phase 6

**Estimated Complexity:** Low

**Definition of Done:**
- [ ] Program accurately extracts brightness and contrast values
- [ ] Decision logic properly flags low-contrast or dark images for CLAHE processing

---

# Phase 8: CLAHE Enhancement

**Status:** ⬜ Not Started

**Objective:** Implement Contrast Limited Adaptive Histogram Equalization (CLAHE) on flagged images.

**Modules Included:**
- `backend/app/utils/image_utils.py`
- `backend/app/pipeline/image_pipeline.py`

**Tasks:**
- Implement RGB to LAB color space conversion
- Apply OpenCV CLAHE to the L-channel using `clip_limit` and `tile_grid_size` from config
- Convert back to RGB and save the enhanced image in `data/temp/`
- Log execution time and metrics to `logs/pipeline.log`

**Deliverables:**
- CLAHE enhancement pipeline stage
- Enhanced image stored in temporary folder

**Dependencies:** Phase 7

**Estimated Complexity:** Low

**Definition of Done:**
- [ ] Dark/low-contrast images are successfully enhanced and saved to `data/temp/<job_id>_enhanced.png`
- [ ] Normal images bypass this stage and return the original image

---

# Phase 9: Florence-2 Caption Generation

**Status:** ⬜ Not Started

**Objective:** Set up Florence-2 model loading, execution, prompt generation, and unloading to free VRAM.

**Modules Included:**
- `ai_models/florence2/`
- `backend/app/pipeline/detection_pipeline.py`

**Tasks:**
- Implement model loader in `ai_models/florence2/loader.py` with GPU offloading and CUDA cache clearing
- Implement caption generator in `ai_models/florence2/caption.py`
- Convert output caption to GroundingDINO dot-separated format (e.g. `a black mug` -> `black . mug`)
- Verify precision options (float16/float32) from configs

**Deliverables:**
- Florence-2 wrapper for captioning
- Text prompt formatted for GroundingDINO

**Dependencies:** Phase 8, Phase 4

**Estimated Complexity:** Medium

**Definition of Done:**
- [ ] Model loads, executes on GPU, unloads, and clears CUDA cache successfully
- [ ] Text caption and GroundingDINO prompt are generated without errors

---

# Phase 10: GroundingDINO Detection

**Status:** ⬜ Not Started

**Objective:** Implement Zero-shot object detection wrapper using GroundingDINO with retry strategy.

**Modules Included:**
- `ai_models/grounding_dino/`
- `backend/app/pipeline/detection_pipeline.py`

**Tasks:**
- Implement model wrapper and loader for GroundingDINO
- Implement 4-pass retry strategy matching confidence thresholds:
  - Pass 1: Original Image, Threshold = 0.20
  - Pass 2: Enhanced Image, Threshold = 0.20 (if CLAHE applied)
  - Pass 3: Enhanced/Original Image, Threshold = 0.15
  - Pass 4: Enhanced/Original Image, Threshold = 0.10
- Save detection visual check to `outputs/images/<job_id>_detection.png` with drawn bounding boxes

**Deliverables:**
- GroundingDINO detector module
- Bounding box coordinates output
- Bounding box overlay validation image

**Dependencies:** Phase 9

**Estimated Complexity:** High

**Definition of Done:**
- [ ] Object is correctly detected with bounding box output coordinates
- [ ] Bounding box verification image is saved to disk
- [ ] Detection retry logic triggers and succeeds when initial threshold fails

---

# Phase 11: Florence-2 Part Detection

**Status:** ⬜ Not Started

**Objective:** Implement object part detection stage using Florence-2.

**Modules Included:**
- `ai_models/florence2/part_detection.py`
- `backend/app/pipeline/detection_pipeline.py`

**Tasks:**
- Implement part detection function using Florence-2's open vocabulary part detection capability
- Extract bounding boxes for major object components (e.g. body, handle, base)
- Save part coordinates in pipeline output metadata

**Deliverables:**
- Object part bounding box detector
- Metadata updated with object part boxes

**Dependencies:** Phase 10

**Estimated Complexity:** Medium

**Definition of Done:**
- [ ] Part detection returns correct bounding box offsets for primary object parts
- [ ] VRAM is cleaned up post-inference

---

# Phase 12: SAM2.1 Segmentation

**Status:** ⬜ Not Started

**Objective:** Implement pixel-accurate instance segmentation utilizing SAM2.1.

**Modules Included:**
- `ai_models/sam2/`
- `backend/app/pipeline/segmentation_pipeline.py`

**Tasks:**
- Implement SAM2.1 loader and wrapper
- Segment primary object using object and part bounding boxes as prompts
- Implement best IoU selection logic from multi-mask output options
- Save binary mask to `data/temp/` and mask overlay image to `outputs/images/<job_id>_segmentation.png`

**Deliverables:**
- SAM2.1 segmentation module
- Binary object mask
- Segmentation visualization image

**Dependencies:** Phase 11

**Estimated Complexity:** High

**Definition of Done:**
- [ ] Multi-mask options generated and highest IoU mask selected
- [ ] Binary mask saved to `data/temp/<job_id>_mask.png`
- [ ] Visualization image saved to `outputs/images/<job_id>_segmentation.png`

---

# Phase 13: Background Removal

**Status:** ⬜ Not Started

**Objective:** Extract target object onto transparent background using `rembg` with ONNX Runtime.

**Modules Included:**
- `ai_models/rembg/`
- `backend/app/pipeline/segmentation_pipeline.py`

**Tasks:**
- Implement `rembg` background removal utility leveraging ONNX Runtime
- Mask out background using the mask generated by SAM2.1
- Save the resulting transparent RGBA image to `outputs/images/<job_id>_rgba.png`

**Deliverables:**
- Background removal module
- Clean transparent RGBA image of the foreground object

**Dependencies:** Phase 12

**Estimated Complexity:** Medium

**Definition of Done:**
- [ ] Output image has exactly 4 channels (RGBA)
- [ ] Transparent background generated correctly with sharp foreground edges
- [ ] Saved output located at `outputs/images/<job_id>_rgba.png`

---

# Phase 14: Hunyuan3D-2 Shape Generation

**Status:** ⬜ Not Started

**Objective:** Generate a watertight 3D mesh geometry from the RGBA image using Hunyuan3D-2.

**Modules Included:**
- `ai_models/hunyuan3d/`
- `backend/app/pipeline/generation_pipeline.py`

**Tasks:**
- Set up Hunyuan3D-2 shape generation model loader with device configuration (CUDA)
- Implement diffusion-based 3D mesh generator from the RGBA image input
- Validate generated mesh contains valid vertices and faces

**Deliverables:**
- Hunyuan3D-2 shape generation wrapper
- Initial untextured mesh geometry

**Dependencies:** Phase 13

**Estimated Complexity:** High

**Definition of Done:**
- [ ] 3D mesh geometry is successfully reconstructed on GPU
- [ ] Mesh is stored in temporary format containing valid geometry elements

---

# Phase 15: Hunyuan3D-2 Texture Generation

**Status:** ⬜ Not Started

**Objective:** Synthesize PBR textures and export the final textured GLB file.

**Modules Included:**
- `ai_models/hunyuan3d/`
- `backend/app/pipeline/generation_pipeline.py`

**Tasks:**
- Set up Hunyuan3D-2 texture generation model loader
- Generate high-fidelity PBR texture mapping aligned with input RGBA appearance
- Package geometry and texture maps into a single self-contained GLB file
- Save output to `outputs/meshes/<job_id>_model.glb`

**Deliverables:**
- Texture synthesis module
- Final textured `model.glb` file

**Dependencies:** Phase 14

**Estimated Complexity:** High

**Definition of Done:**
- [ ] Self-contained GLB mesh generated and saved to `outputs/meshes/<job_id>_model.glb`
- [ ] File size and readability verified

---

# Phase 16: Mesh Processing (Open3D Validation)

**Status:** ⬜ Not Started

**Objective:** Perform mesh validation and normal computation using Open3D.

**Modules Included:**
- `backend/app/services/mesh_service.py`
- `backend/app/utils/mesh_utils.py`

**Tasks:**
- Implement Open3D mesh loading and sanity checks
- Programmatic validation: check for missing geometry, ensure watertightness
- Compute vertex normals and orient them correctly

**Deliverables:**
- Open3D mesh validation service
- Validated mesh metrics registered in job metadata

**Dependencies:** Phase 15

**Estimated Complexity:** Medium

**Definition of Done:**
- [ ] Mesh parses through Open3D without errors
- [ ] Vertex normals are computed and output status validated

---

# Phase 17: Point Cloud Generation

**Status:** ⬜ Not Started

**Objective:** Convert the 3D mesh into a dense point cloud using Poisson Disk Sampling.

**Modules Included:**
- `backend/app/services/pointcloud_service.py`
- `backend/app/utils/pointcloud_utils.py`

**Tasks:**
- Implement Poisson Disk Sampling algorithm using Open3D
- Sample target number of points (default 100,000) from the mesh surface
- Estimate and orient point cloud normals
- Save output raw point cloud to `outputs/pointcloud/<job_id>_pointcloud.ply`

**Deliverables:**
- Poisson Disk Sampling point cloud generator
- High-density raw PLY point cloud file

**Dependencies:** Phase 16

**Estimated Complexity:** Medium

**Definition of Done:**
- [ ] PLY file successfully created at `outputs/pointcloud/<job_id>_pointcloud.ply`
- [ ] File contains target points with valid X, Y, Z, R, G, B channels and normals

---

# Phase 18: DBSCAN Segmentation

**Status:** ⬜ Not Started

**Objective:** Segment the generated point cloud into spatial/semantic clusters using DBSCAN.

**Modules Included:**
- `backend/app/services/pointcloud_service.py`
- `backend/app/pipeline/pointcloud_pipeline.py`

**Tasks:**
- Implement DBSCAN clustering algorithm using Open3D or scikit-learn matching configs
- Extract cluster labels and assign distinct color mappings to different clusters
- Save the segmented point cloud to `outputs/pointcloud/<job_id>_segmented_pointcloud.ply`

**Deliverables:**
- DBSCAN clustering processor
- Clustered and colored PLY point cloud file

**Dependencies:** Phase 17

**Estimated Complexity:** Medium

**Definition of Done:**
- [ ] DBSCAN successfully clusters points with outliers removed if configured
- [ ] Clustered point cloud saved at `outputs/pointcloud/<job_id>_segmented_pointcloud.ply`

---

# Phase 19: 3D Viewer

**Status:** ⬜ Not Started

**Objective:** Implement interactive 3D mesh visualization in the frontend results page.

**Modules Included:**
- `frontend/components/Viewer/`
- `frontend/app/viewer/`

**Tasks:**
- Implement a Three.js / React Three Fiber viewer component with OrbitControls
- Add camera helper features (auto-fit, zoom, pan, rotate, camera reset)
- Bind the viewer to load and render the generated GLB model from the job results endpoint
- Add point cloud rendering mode option in the viewer

**Deliverables:**
- React Three Fiber interactive 3D viewer component
- Multi-mode rendering controls (Mesh / Point Cloud)

**Dependencies:** Phase 3, Phase 15, Phase 17

**Estimated Complexity:** Medium

**Definition of Done:**
- [ ] Viewer successfully loads and displays target GLB meshes
- [ ] User can orbit, zoom, pan, and switch rendering modes on the UI

---

# Phase 20: Download & Status APIs

**Status:** ⬜ Not Started

**Objective:** Implement API endpoints to check progress and download generated artifacts.

**Modules Included:**
- `backend/app/api/pipeline.py`
- `backend/app/api/download.py`
- `backend/app/controllers/pipeline_controller.py`
- `backend/app/controllers/download_controller.py`
- `frontend/components/Progress/`
- `frontend/components/Download/`

**Tasks:**
- Implement GET status API endpoint `/api/v1/pipeline/status/{job_id}` returning progress values (0% - 100%)
- Implement file download endpoints for GLB, PLY, RGBA, Detection, Segmentation, and Metadata reports
- Implement frontend polling service calling progress status
- Create the Download Panel UI showing list of artifacts with download buttons

**Deliverables:**
- Download routes serving files as attachments
- Polling mechanism updating frontend processing screen
- Download panel component

**Dependencies:** Phase 5, Phase 18, Phase 19

**Estimated Complexity:** Medium

**Definition of Done:**
- [ ] Progress endpoint returns correct stage-bound percentage values
- [ ] All download buttons retrieve corresponding generated files from `outputs/`
- [ ] Polling stops and redirects to results page once progress reaches 100%

---

# Phase 21: Testing

**Status:** ⬜ Not Started

**Objective:** Write and execute automated unit, integration, and performance tests.

**Modules Included:**
- `tests/`

**Tasks:**
- Write backend test suites using `pytest` for all helper utilities and pipeline stages
- Set up integration tests covering sequential model loading/unloading flow
- Write UI integration tests using Playwright
- Measure pipeline execution times to verify compliance with performance specifications

**Deliverables:**
- Automated test scripts
- Test coverage and performance report

**Dependencies:** Phase 20

**Estimated Complexity:** Medium

**Definition of Done:**
- [ ] All unit and integration tests execute and pass successfully
- [ ] Pipeline total duration is confirmed to be under 4 minutes on a CUDA-enabled GPU

---

# Phase 22: Optimization

**Status:** ⬜ Not Started

**Objective:** Perform memory optimization, model cache clearing, and performance profiling.

**Modules Included:**
- `backend/app/core/settings.py`
- `backend/app/pipeline/pipeline_manager.py`

**Tasks:**
- Audit VRAM footprint during full execution
- Confirm absolute release of VRAM variables and model weights after each stage via garbage collection and `torch.cuda.empty_cache()`
- Optimize image scaling configurations for low-spec setups

**Deliverables:**
- VRAM optimization profiling report
- Resource leakage prevention code updates

**Dependencies:** Phase 21

**Estimated Complexity:** Medium

**Definition of Done:**
- [ ] VRAM peaks remain below the configured threshold
- [ ] Memory footprint does not grow during consecutive job executions

---

# Phase 23: Final Verification

**Status:** ⬜ Not Started

**Objective:** Perform end-to-end user verification and final compliance checks.

**Modules Included:**
- Complete codebase

**Tasks:**
- Run complete end-to-end pipeline verification on sample images
- Check all output directories for files matching success criteria:
  - `detection.png`
  - `segmentation.png`
  - `rgba.png`
  - `model.glb`
  - `pointcloud.ply`
  - `segmented_pointcloud.ply`
  - `result.json`
- Ensure no build, linting, or runtime errors are present

**Deliverables:**
- Verified end-to-end running system
- Final completion summary

**Dependencies:** Phase 22

**Estimated Complexity:** Medium

**Definition of Done:**
- [ ] End-to-end system produces all 7 outputs without exceptions
- [ ] Code compiles cleanly with zero errors
- [ ] Implementation plan updated with `🟩 Completed` statuses
