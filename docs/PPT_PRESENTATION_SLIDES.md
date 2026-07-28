# KLE Society's

# KLE Technological University, Hubballi

## Department Of MCA — IV Semester

---

# Presentation Slide Deck

## On

## “Automated Single-Image to 3D Asset and Point Cloud Generation System”

**Submitted by:**
Rajashekhar B Durgad (01FE24MCA027)

**Under the Guidance of:**
Prof. Akash Hulkund

---

## Agenda

1. Introduction
2. Problem Statement
3. Objectives
4. Scope and Constraints
5. Block Diagram
6. Requirements
   - 6.1 Functional Requirements
   - 6.2 Non-functional Requirements
7. Use-case Diagram
8. Conclusion and Future Scope
9. References

---

# Slide 1: Introduction

- **Overview:**
  - Automated web application converting a single 2D RGB photograph into a textured 3D polygon mesh (`.GLB`) and a 3D surface point cloud (`.PLY`).
  - Eliminates traditional manual 3D modeling overhead through a fast feed-forward Generative AI pipeline.
- **Core Multi-Stage Engine:**
  - Meta SAM 2.1 for zero-shot foreground object isolation and alpha matting.
  - Tencent Hunyuan3D-2 for rapid triplane mesh reconstruction (~15s).
  - Open3D for uniform 10,000-point Poisson disk sampling and surface normal estimation.
- **Web Application Architecture:**
  - Next.js 15 (React 19, TypeScript, Tailwind CSS) frontend with React Three Fiber (R3F) 60 FPS WebGL viewer.
  - Asynchronous FastAPI backend managing PyTorch CUDA 12.1 model inference and Supabase cloud storage.

---

# Slide 2: Problem Statement

- **High Barrier to Entry in 3D Modeling:**
  - Traditional 3D content creation requires specialized CAD software (Blender, Maya) and manual artistic labor taking hours to days per asset.
- **Photogrammetry & Text-to-3D Limitations:**
  - Multi-view photogrammetry demands 50+ calibrated camera angles and studio lighting setups.
  - Text-to-3D generative tools introduce spatial ambiguity and fail to replicate specific physical real-world objects.
- **Hardware & Memory Bottlenecks:**
  - Deep learning 3D reconstruction models frequently cause out-of-memory (OOM) crashes on standard GPU workstation environments.
- **The Core Goal:**
  - Develop a non-intrusive, prompt-free, single-photograph 2D-to-3D synthesis web system running within a 16 GB GPU VRAM cap.

---

# Slide 3: Objectives

- **Primary System Objectives:**
  - **Prompt-Free 2D-to-3D Pipeline:** Automate single RGB image ingestion without requiring text prompts or manual masks.
  - **Zero-Shot Foreground Segmentation:** Isolate background clutter using Meta SAM 2.1 to generate clean RGBA cutouts.
  - **Rapid 3D Mesh Synthesis:** Generate textured watertight `.GLB` polygon meshes in ~15 seconds using Hunyuan3D-2.
  - **Point Cloud Extraction:** Generate 10,000 uniform surface points with estimated $k$-NN surface normal vectors (`.PLY`).
  - **Interactive 60 FPS WebGL Viewer:** Build a responsive browser canvas (Next.js 15 + R3F) supporting orbit controls and Light/Dark themes.
  - **GPU VRAM Optimization:** Ensure sequential pipeline execution keeps peak GPU memory below 16 GB VRAM (achieved 11.4 GB).

---

# Slide 4: Scope and Constraints

- **System Scope:**
  - **Input Formats:** Single 2D RGB photograph (JPG, PNG, WEBP, BMP) up to 25 MB.
  - **Output Assets:** Downloadable textured `.GLB` mesh, `.PLY` point cloud with normals, RGBA cutout, and JSON metadata.
  - **Target Domains:** E-commerce 3D product catalogs, AR/VR spatial applications, game development, and educational tools.
- **System Constraints:**
  - **Single Foreground Subject:** Optimized for single prominent objects rather than complex multi-object room scenes.
  - **Hardware Boundary:** Designed for execution within a 16 GB VRAM GPU ceiling (NVIDIA T4 workstation).
  - **Texture Interpolation:** Occluded rear surfaces are synthesized using generative triplane diffusion interpolation.

---

# Slide 5: Block Diagram

```
+-----------------------------------------------------------------------------------+
|                                 CLIENT VIEWPORT                                   |
|   +---------------------------------------------------------------------------+   |
|   | Next.js 15 Web Dashboard (React 19 / React Three Fiber 60 FPS Canvas)     |   |
|   +---------------------------------------------------------------------------+   |
+------------------------------------------+----------------------------------------+
                                           | HTTP / REST API (JWT Auth)
                                           v
+-----------------------------------------------------------------------------------+
|                             FASTAPI ASYNC BACKEND SERVER                          |
|   +---------------------------------------------------------------------------+   |
|   | Job Orchestrator & Storage Manager (PyTorch / CUDA 12.1 Engine)           |   |
|   +---------------------------------------------------------------------------+   |
+------------------------------------------+----------------------------------------+
                                           | Sequential CUDA Execution
                                           v
+-----------------------------------------------------------------------------------+
|                             GENERATIVE AI MODEL PIPELINE                          |
|                                                                                   |
|  [ Stage 1: SAM 2.1 ] ----> [ Stage 2: Hunyuan3D-2 ] ----> [ Stage 3: Open3D ]    |
|  Foreground Cutout           Textured .GLB Mesh             10k .PLY Point Cloud  |
|                                                                                   |
+------------------------------------------+----------------------------------------+
                                           | Persistent Storage
                                           v
+-----------------------------------------------------------------------------------+
|                         SUPABASE CLOUD DATABASE & STORAGE                         |
|   PostgreSQL Jobs Table  |  Row Level Security (RLS)  |  Object Storage Buckets |
+-----------------------------------------------------------------------------------+
```

---

# Slide 6: Requirements

## 6.1 Functional Requirements

- **FR-01 (Authentication):** Secure user login and registration issuing signed Supabase JWT session tokens.
- **FR-02 (Image Ingestion):** Drag-and-drop file upload supporting format validation (JPG/PNG/WEBP) and 25 MB size capping.
- **FR-03 (Segmentation):** Automated zero-shot background removal and RGBA cutout generation via Meta SAM 2.1.
- **FR-04 (Mesh Reconstruction):** Synthesize textured 3D polygon meshes exported as standardized `.GLB` files.
- **FR-05 (Point Cloud Extraction):** Poisson disk surface sampling generating 10,000 points with $k$-NN normal vectors (`.PLY`).
- **FR-06 (3D Canvas):** Interactive WebGL 3D canvas with 60 FPS orbit rotation, panning, zoom controls, and theme toggling.

## 6.2 Non-functional Requirements

- **Performance:** End-to-end pipeline execution completed in **~19.6 seconds**.
- **Memory Control:** Peak GPU memory usage strictly kept at **11.4 GB VRAM** (under the 16 GB ceiling).
- **Usability & Aesthetics:** Modern glassmorphism UI supporting seamless Light/Dark mode transitions.

---

# Slide 7: Use-case Diagram

```
                              +-------------------------------------------+
                              |         SINGLE-IMAGE 3D SYSTEM            |
                              |                                           |
    +--------------+          |  (UC-01: User Login / Register)           |          +------------------+
    |              | -------- |                                           | -------- |                  |
    |              | -------- |  (UC-02: Upload Single RGB Image)         | -------- |                  |
    |    USER      |          |                                           |          |  FASTAPI BACKEND |
    |   (Client)   | -------- |  (UC-03: Track Processing Progress)       | -------- |    & AI MODELS   |
    |              |          |                                           |          |                  |
    |              | -------- |  (UC-04: Interact with WebGL 3D Canvas)   | -------- |                  |
    |              | -------- |                                           |          |                  |
    +--------------+          |  (UC-05: Download GLB / PLY Assets)       |          +------------------+
                              |                                           |
                              +-------------------------------------------+
```

- **Actor - User:** Registers, uploads photographs, monitors real-time processing status, manipulates the 3D model, and exports files.
- **Actor - Backend System:** Validates authentication, enqueues job states, executes AI model stages sequentially, and persists artifacts.

---

# Slide 8: Conclusion and Future Scope

- **Conclusion:**

  - Successfully engineered an end-to-end automated 2D-to-3D asset and point cloud generation web system.
  - Achieved fast processing (**~19.6 seconds**) and low GPU memory footprint (**11.4 GB VRAM**) on commodity hardware.
  - Delivered production-ready textured `.GLB` meshes and 10,000-point `.PLY` surface point clouds.
- **Future Scope & Enhancements:**

  - **PBR Material Synthesis:** Generate Physically-Based Rendering channels (metallic, roughness, ambient occlusion, normal maps).
  - **Real-Time WebGPU Gaussian Splatting:** Implement 3D Gaussian Splatting for photorealistic volumetric radiance field rendering.
  - **CAD Topology Optimization:** Quad-mesh remashing for watertight `.STL` 3D printing export.
  - **WebXR AR/VR Integration:** Real-world mobile camera passthrough and Apple Vision Pro augmented reality asset placement.

---

# Slide 9: References

1. **Tencent Hunyuan3D-2 Team. (2025).** *Hunyuan3D 2.0: Scaling Diffusion Models for High-Fidelity 3D Asset Generation*. arXiv:2501.12211.
2. **Kirillov, A., et al. (2023).** “Segment Anything.” *IEEE/CVF ICCV*, pp. 4015–4026.
3. **Ravi, N., et al. (2024).** *SAM 2: Segment Anything in Images and Videos*. arXiv:2408.00714.
4. **Li, J., et al. (2022).** “BLIP: Bootstrapping Language-Image Pre-training.” *ICML*, 12888–12900.
5. **Zhou, Q., et al. (2018).** *Open3D: A Modern Library for 3D Data Processing*. arXiv:1801.09847.
6. **Lorensen, W. E., & Cline, H. E. (1987).** “Marching Cubes: A 3D Surface Construction Algorithm.” *ACM SIGGRAPH*, 21(4), 163–169.
7. **Next.js & React Three Fiber Documentation. (2025).** Vercel & Poimandres. https://nextjs.org/docs
