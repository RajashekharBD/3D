# KLE Society's

# KLE Technological University, Hubballi

## Department Of MCA

### MCA IV Semester

# CHAPTER – 6

# TESTING

## On

# “Automated Single-Image to 3D Asset and Point Cloud Generation System”

**Submitted by:**
Rajashekhar B Durgad (01FE24MCA027)

**Under the Guidance of:**
Prof. Akash Hulkund

**KLE Technological University**
Vidyanagar, Hubballi – 580031
2025-2026

---

## 6.1 Test Plan and Test Cases

Software testing is a critical phase in the software development lifecycle that ensures the system operates reliably, satisfies functional requirements, and adheres to performance and security constraints. For the Automated Single-Image to 3D Asset and Point Cloud Generation System, a comprehensive testing strategy was established combining **Unit Testing**, **Integration Testing**, **GPU Memory Stress Testing**, and **Acceptance Testing**.

### 6.1.1 Testing Strategy & Testing Levels

Four testing levels were applied throughout the development of this system:

* **Unit Testing:** Individual functions — such as the JWT token verifier, image format validator, magic header byte inspector, and Open3D normal estimator — were verified in isolation to confirm correct output for a range of inputs.
* **Integration Testing:** The interaction between the Next.js Web Frontend, FastAPI API Gateway, Supabase Auth/Database, and GPU Worker Node pipeline was tested end-to-end, with particular focus on the 4-stage AI reconstruction pipeline.
* **System Testing:** Black-box testing was performed on a GPU-enabled workstation with WebGL 2.0. A tester interacted only with the web interface, simulating real user single-image upload and 3D asset generation across all functional scenarios.
* **User Acceptance Testing (UAT):** Informal UAT was conducted with a group of end-users (3D designers/developers), who confirmed the interface is intuitive and the generated 3D meshes (`.GLB`) and point clouds (`.PLY`) satisfy 3D asset creation needs.

All tests were executed on a GPU compute node (NVIDIA T4 16GB VRAM) and WebGL-enabled browser, as PyTorch CUDA model inference and WebGL 3D rendering require dedicated hardware execution environments.

---

### 6.1.2 Test Environment Configuration

| Component                           | Test Environment Specification         |
| :---------------------------------- | :------------------------------------- |
| **Operating System**          | Ubuntu 22.04 LTS / Windows 11          |
| **GPU Compute Node**          | NVIDIA T4 GPU (16 GB VRAM)             |
| **CUDA Runtime**              | CUDA 12.1 / PyTorch 2.x                |
| **Backend Testing Framework** | `pytest`, FastAPI `TestClient`     |
| **Database & Auth Services**  | Supabase (PostgreSQL), Supabase Auth   |
| **Browser Environment**       | Google Chrome 125+ (WebGL 2.0 Enabled) |

---

### 6.1.3 Acceptance Test Execution & Specification Matrix

The master table below summarizes the test scenarios, input data, expected results, actual observed results, and pass/fail status for all 8 acceptance tests defined in Chapter 3. All test scenarios achieved a **100% Pass Rate**.

|     Test ID     | Test Scenario                     | Component Tested    | Input Data                                             | Expected Output                              | Actual Output                                  |     Status     |
| :-------------: | :-------------------------------- | :------------------ | :----------------------------------------------------- | :------------------------------------------- | :--------------------------------------------- | :------------: |
| **TC-01** | User Registration & Login         | `AuthController`  | Email:`user@example.com`, Password: `Password123!` | Authenticated; signed JWT token issued       | JWT token issued; dashboard loaded             | **PASS** |
| **TC-02** | Valid Image Upload & Job Creation | `ImageValidator`  | File:`sample.png` (4.2 MB, valid format)             | Image validated; job status set to`QUEUED` | Job created; redirected to processing page     | **PASS** |
| **TC-03** | Format & Size Limit Validation    | `ImageValidator`  | File:`doc.pdf` OR file > 25 MB                       | Upload rejected; HTTP 400 error              | Error displayed: "File format or size invalid" | **PASS** |
| **TC-04** | AI Pipeline Progress Tracking     | `PipelineManager` | Enqueued Job ID (polling interval: 2s)                 | Progress updates live 0% to 100%             | Live status returned: 20%, 40%, 75%, 100%      | **PASS** |
| **TC-05** | Interactive 3D Mesh Rendering     | WebGL R3F Canvas    | Artifact URL:`job_123.glb`                           | GLB 3D mesh renders with orbit controls      | Mesh renders at 60 FPS with OrbitControls      | **PASS** |
| **TC-06** | Point Cloud Visualization         | Open3D Renderer     | User clicks "Point Cloud View"                         | Canvas renders 3D point cloud with normals   | Point cloud vertices & normals rendered        | **PASS** |
| **TC-07** | Multi-Format Artifact Export      | Supabase Storage    | Request:`GLB`, `PLY`, `PNG`, `JSON`            | Supabase RLS verifies; files stream          | All 4 files downloaded without corruption      | **PASS** |
| **TC-08** | Job History & Filtering           | History Component   | Search query:`"chair"`, Status: `COMPLETED`        | Matching job cards rendered in grid          | Filtered job grid displayed accurately         | **PASS** |

---

## 6.2 Edge Case & Negative Testing

Beyond standard operational flows, robust systems must gracefully handle unexpected inputs, resource exhaustion, and hardware failures. The edge cases detailed below were specifically designed to challenge the system's error-handling boundaries and validate its fault tolerance.

| EC ID | Scenario | Condition | Expected Behavior | Observed Result | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **EC-01** | Corrupted Image Header | File named `.png` containing plain text | Header validation rejects file; HTTP 400 | Validation error shown; upload aborted | **PASS** |
| **EC-02** | Over-sized File Upload | Image file exceeding 25 MB cap | Middleware blocks upload before storage | Intercepted with size limit error | **PASS** |
| **EC-03** | GPU VRAM Exhaustion Risk | Sequential model execution under peak load | `torch.cuda.empty_cache()` prevents OOM | Peak memory stayed < 16 GB VRAM | **PASS** |
| **EC-04** | Cluttered / Low-Contrast Input | Input image with complex background | SAM isolates primary salient object | Background stripped cleanly | **PASS** |
| **EC-05** | Storage Disconnection Mid-Job | Database connection lost during export | Job marked `FAILED`; error logged | Job state set to `FAILED` gracefully | **PASS** |
| **EC-06** | Browser Disconnection | User closes browser during generation | GPU worker finishes; saves in DB | Job completed; available on relaunch | **PASS** |
| **EC-07** | Network Timeout on 3D Stream | Interrupted stream during GLB download | WebGL viewer shows graceful error UI | Loading error fallback rendered | **PASS** |
| **EC-08** | Rapid Burst Submissions | User clicks submit 5 times rapidly | Submit button disabled; rate-limited | Single job enqueued; duplicates blocked | **PASS** |

---

## 6.3 Test Results Summary

Synthesizing the outcomes from all testing phases provides a clear indicator of the system's overall reliability and readiness for deployment. The summary dashboard below aggregates the results across all categories.

| Testing Category | Test Case Ref. | Total Cases | Passed | Failed | Pass Rate |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **User Authentication & Security** | TC-01 | 1 | 1 | 0 | 100% |
| **Image Ingestion & Validation** | TC-02, TC-03 | 2 | 2 | 0 | 100% |
| **AI Reconstruction Pipeline** | TC-04 | 1 | 1 | 0 | 100% |
| **3D Visualization & Export** | TC-05, TC-06, TC-07, TC-08 | 4 | 4 | 0 | 100% |
| **Edge & Negative Cases** | EC-01 – EC-08 | 8 | 8 | 0 | 100% |
| **Total Overall System Tests** | **All Categories** | **16** | **16** | **0** | **100%** |

All 16 test cases passed. The sequential model pipeline execution and explicit GPU memory cache clearing (`torch.cuda.empty_cache()`) were the primary contributors to system reliability — preventing GPU Out-Of-Memory (OOM) crashes even during heavy multi-view mesh synthesis, while automated input validation prevented invalid file execution.
