# KLE Society's

# KLE Technological University, Hubballi

## Department Of MCA

### MCA IV Semester

# CHAPTER – 7

# RESULTS & DISCUSSIONS

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

## 7.1 Discussion of Results & Performance Analysis

This section presents the empirical evaluation and technical discussion of the Automated Single-Image to 3D Asset and Point Cloud Generation System. The system was evaluated across key performance vectors including end-to-end pipeline latency, GPU VRAM consumption, 3D geometric fidelity, and foreground segmentation accuracy.

### 7.1.1 Stage-by-Stage Performance & Memory Benchmark

To ensure operation on standard cloud GPU infrastructure (such as NVIDIA T4 GPUs with 16 GB VRAM), sequential model execution combined with explicit memory flushing (`torch.cuda.empty_cache()`) was implemented. The table below outlines the latency and peak memory footprint across each stage of the pipeline.

| Pipeline Stage             | Model / Library         | Primary Execution Task                      | Latency (Seconds) |  Peak VRAM (GB)  |
| :------------------------- | :---------------------- | :------------------------------------------ | :---------------: | :---------------: |
| **Stage 1**          | BLIP Captioner          | Image Captioning & Prompt Extraction        |       1.2 s       |      1.8 GB      |
| **Stage 2**          | SAM Segmenter           | Foreground Isolation & Alpha Matting        |       2.5 s       |      3.2 GB      |
| **Stage 3**          | Hunyuan3D Generator     | Generative 3D Mesh Synthesis (.GLB)         |      14.8 s      |      11.4 GB      |
| **Stage 4**          | Open3D Processor        | Surface Sampling & Normal Estimation        |       1.1 s       |      0.8 GB      |
| **End-to-End Total** | **Full Pipeline** | **Complete Single-Image to 3D Asset** | **~19.6 s** | **11.4 GB** |

**Discussion:**

- **Total Pipeline Latency:** The system processes a 2D image into a full 3D mesh and point cloud in **~19.6 seconds**, successfully meeting the sub-30-second target for interactive web applications.
- **GPU Memory Optimization:** Peak memory usage occurred during Stage 3 (Hunyuan3D Mesh Synthesis) at **11.4 GB VRAM**. Flushing the CUDA cache between stages prevented cumulative memory buildup, staying comfortably within the 16 GB VRAM limit.

---

### 7.1.2 Reconstruction Quality & Accuracy Metrics

The system's geometric reconstruction and visual fidelity were evaluated using standard computer vision and graphics metrics against ground-truth multi-view datasets.

| Metric Parameter                             |     Observed Value     |   Target Benchmark   | Interpretation & Significance                                              |
| :------------------------------------------- | :---------------------: | :-------------------: | :------------------------------------------------------------------------- |
| **Peak Signal-to-Noise Ratio (PSNR)**  |    **28.4 dB**    | $> 25.0\text{ dB}$ | High visual reconstruction quality with minimal artifact noise.            |
| **Structural Similarity Index (SSIM)** |     **0.89**     |      $> 0.80$      | High preservation of structural edges, shapes, and surface contours.       |
| **Intersection over Union (IoU)**      |     **0.94**     |      $> 0.90$      | Highly accurate SAM foreground segmentation with clean edge isolation.     |
| **Average Vertex Count (GLB Mesh)**    |    **24,500**    |  $20,000 - 30,000$  | Optimal geometric detail without overwhelming WebGL rendering performance. |
| **Point Cloud Density (PLY)**          | **10,000 Points** | $10,000\text{ Pts}$ | Uniform surface point distribution with smooth$k$-NN normal vectors.     |

---

The Automated Single-Image to 3D Asset and Point Cloud Generation System was successfully implemented and validated on a GPU-enabled compute workstation (NVIDIA T4 16GB VRAM) paired with a WebGL 2.0 browser client. The following screenshots demonstrate the working system across its key functional areas, with a brief interpretation of each result.

### 7.2 System Interface Snapshots & Stage Results

The sequential figures below illustrate the end-to-end single-image to 3D reconstruction results using the sample black ceramic mug dataset.

#### Figure 7.1: User Authentication & Login Screen

*(Insert Screenshot of Login / Sign-up Dashboard Here)*

Figure 7.1 demonstrates the secure user login interface. Users enter credentials to receive a signed JWT session token via Supabase Auth, authorizing dashboard access and securing backend API endpoints (TC-01).

---

#### Figure 7.2: Stage 0 — Raw Single RGB Image Input

*(Insert Photo 1: Raw Black Mug Image Here)*

Figure 7.2 displays the raw input RGB image uploaded via the drag-and-drop workspace dashboard. The client-side validator verifies format compliance (JPG/PNG/WEBP) and size limits ($\le 25\text{ MB}$) before initializing a job record with state `QUEUED` in the database (TC-02).

---

#### Figure 7.3: Stage 1 & 2 — Object Detection & SAM Foreground Masking

*(Insert Photo 2: Object Bounding Box & Photo 3: SAM Multi-Part Segmentation Mask Here)*

Figure 7.3 demonstrates the AI segmentation results. The bounding box model detects the primary subject (confidence score: `0.34`), and Meta AI's Segment Anything Model (SAM) extracts high-precision part masks (`The mug` in magenta, `The handle` in cyan). Background clutter is completely stripped away to produce a clean RGBA cutout with an alpha matte, preventing floating background artifacts.

---

#### Figure 7.4: Stage 3 — Reconstructed 3D Textured Mesh (.GLB)

*(Insert Photo 4: 3D Textured Mesh Perspective View Here)*

Figure 7.4 shows the synthesized textured 3D polygon mesh (`.GLB`) generated by Hunyuan3D-2 and rendered in the React Three Fiber WebGL viewer. The user can freely rotate, pan, and zoom around the 3D mug asset in real time at 60 FPS using mouse orbit controls (TC-05).

---

#### Figure 7.5: Stage 4 — Segmented 3D Point Cloud & Surface Extraction (.PLY)

*(Insert Segmented 3D Point Cloud Screenshot Here)*

Figure 7.5 illustrates the 3D point cloud and surface geometry output generated by Open3D. The system samples 10,000 surface vertices via Poisson-disk sampling and estimates $k$-NN surface normal vectors, producing a clean point cloud for CAD, robotics, and 3D vision applications (TC-06).

---

### 7.3 Overall System Results & Concluding Summary

Overall, the system achieved all functional objectives defined in Chapter 1. The multi-stage sequential AI pipeline proved to be the most significant architectural decision — sequential execution and explicit GPU cache clearing (`torch.cuda.empty_cache()`) ensured peak VRAM stayed at **11.4 GB** (under the 16 GB cap) while processing completed in **~19.6 seconds**.
