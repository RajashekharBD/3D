# KLE Society's
# KLE Technological University, Hubballi
## Department Of MCA
### MCA IV Semester

# 1. Introduction

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

## 1.1 Introduction

Three-dimensional (3D) content has become a foundational element across numerous industries, including e-commerce, augmented reality (AR), virtual reality (VR), robotics, digital twins, and industrial inspection. The demand for high-quality 3D assets has grown exponentially with the expansion of the metaverse, web-based 3D applications, and automated manufacturing workflows. However, traditional 3D asset creation remains a labour-intensive process requiring either multi-view photogrammetry setups, manual 3D modelling expertise, or text-prompted generative pipelines that depend on carefully crafted descriptions.

The **Automated Single-Image to 3D Asset and Point Cloud Generation System** addresses these challenges by providing a fully automated, prompt-free pipeline that converts a single RGB image into a production-ready textured 3D mesh and a geometrically segmented point cloud. The system integrates five state-of-the-art AI foundation models—Florence-2, GroundingDINO, SAM2.1, rembg, and Hunyuan3D-2—into a unified orchestration layer with sequential GPU memory management, enabling the entire pipeline to execute on a single GPU with 16 GB of VRAM.

This report documents the complete design, implementation, testing, and results of the system. Chapter 2 presents a literature survey of related work. Chapter 3 describes the system analysis and architecture. Chapter 4 details the implementation. Chapter 5 presents testing and results. Chapter 6 concludes the report with a summary and future scope.

## 1.2 Background of the Study

The creation of 3D content has historically been confined to specialists using complex tools such as Blender, Autodesk Maya, or 3ds Max. Photogrammetry offered a path to automate reconstruction, but required multiple camera angles, controlled lighting, and significant post-processing. The emergence of deep learning-based generative models has opened new possibilities for single-image 3D reconstruction, but these models remain fragmented across separate research domains.

Vision-language models (VLMs) such as Florence-2 and GroundingDINO have advanced the ability to understand and describe image content without task-specific training. Segmentation models like SAM2.1 provide zero-shot instance segmentation with remarkable accuracy. Generative 3D frameworks such as Hunyuan3D-2 can produce high-fidelity textured meshes from clean RGBA inputs. However, no unified system existed that combined these capabilities into an automated end-to-end pipeline with efficient resource management and a production-ready web interface.

This project bridges that gap by integrating these state-of-the-art models into a single cohesive system, adding adaptive preprocessing, sequential VRAM management, and a full-stack web application with user authentication and job history.

## 1.3 Problem Statement

Despite significant advances in generative AI and computer vision, existing 3D reconstruction workflows suffer from several critical limitations:

- **Multi-View Dependency:** Traditional photogrammetry solutions require multiple images captured from different angles under controlled lighting conditions, making them impractical for rapid asset generation from a single photograph.
- **Manual Prompting:** High-quality 3D generators typically require users to provide detailed text descriptions to guide shape and texture synthesis, adding friction to the workflow.
- **Pipeline Fragmentation:** Object detection, segmentation, 3D generation, and point cloud analysis are handled by separate tools requiring manual data transfer between stages, increasing complexity and error rates.
- **High Hardware Requirements:** Running multiple deep learning models concurrently leads to out-of-memory (OOM) failures on standard GPUs, limiting accessibility.
- **Single-Format Outputs:** Most existing solutions produce either a mesh or a point cloud, but not both with geometric segmentation in a single run, forcing users to use additional tools for downstream analysis.

There is a need for a unified, automated system that can accept a single image and produce both a textured 3D mesh and a segmented point cloud without manual intervention, while managing hardware resources efficiently and providing a polished user interface.

## 1.4 Objectives of the Project

The primary objectives of this project are:

1. **Adaptive Image Preprocessing:** Automatically analyse input brightness and contrast, applying CLAHE enhancement only when necessary to improve detection accuracy for dark or low-contrast images.

2. **Prompt-Free Operation:** Generate natural language captions and detection prompts automatically using Florence-2, eliminating the need for manual text input.

3. **Zero-Shot Object Detection and Segmentation:** Detect the primary object in the image using GroundingDINO with multi-pass threshold retries, and generate pixel-precise masks using SAM2.1.

4. **Automated Background Removal:** Remove the background using rembg with ONNX Runtime, refined by the SAM2.1 binary mask for clean RGBA output.

5. **Generative 3D Reconstruction:** Produce a watertight, textured 3D mesh in GLB format using the Hunyuan3D-2 diffusion transformer framework.

6. **Point Cloud Generation and Segmentation:** Sample the mesh surface using Poisson-disk sampling, estimate surface normals, and segment the point cloud into geometrically meaningful clusters using DBSCAN.

7. **Secure User Access:** Provide user authentication and session management via Supabase Auth with JWT tokens.

8. **Persistent Job History:** Store pipeline execution records, generated artifact metadata, and user profiles in a Supabase PostgreSQL database with row-level security.

9. **Interactive Web Interface:** Deliver a responsive frontend with real-time pipeline progress tracking, interactive 3D mesh and point cloud viewing, and downloadable output artifacts.

## 1.5 Scope of the Project

The scope of this project encompasses the full vertical integration of multiple AI models into a single production-grade system:

- **Input:** Single RGB images in standard formats (JPEG, PNG, WebP, BMP) up to 25 MB.
- **Processing:** An orchestrated pipeline comprising image analysis, adaptive enhancement, vision-language captioning, object detection, part detection, instance segmentation, background removal, 3D shape generation, texture synthesis, mesh validation, point cloud sampling, and geometric clustering.
- **Outputs:** Textured GLB mesh, raw and segmented PLY point clouds, debug visualizations (detection, segmentation, mask overlays), and structured JSON metadata.
- **User Interface:** A Next.js web application with authentication flows, upload interface, real-time progress tracking, 3D viewer, job history dashboard, and user profile management.
- **API:** A FastAPI backend exposing RESTful endpoints for upload, pipeline status polling, artifact download, history management, and profile operations, all secured via JWT authentication.

The system is designed for single-object reconstruction from a single viewpoint. Multi-object scenes and video-to-3D reconstruction are outside the current scope.

## 1.6 Motivation

The motivation for this project stems from the growing demand for rapid 3D content creation across multiple industries:

- **E-commerce:** Online retailers require 3D product models for interactive product viewers, but traditional 3D modelling is prohibitively expensive for catalog-scale deployment.
- **AR/VR Applications:** Augmented and virtual reality applications need large libraries of 3D assets, but manual creation cannot keep pace with content demands.
- **Robotics and Automation:** Robotic systems require 3D understanding of objects for grasping and manipulation, but existing pipelines are too slow for real-time adaptation.
- **Education and Research:** Students and researchers need accessible tools to experiment with 3D reconstruction without specialized hardware or expertise.
- **Accessibility:** Non-technical users such as designers, artists, and hobbyists lack tools to convert photographs into 3D models without learning complex 3D software.

By providing a fully automated, single-click solution accessible through a web browser, this project aims to democratize 3D content creation and make it available to a broader audience.

## 1.7 Methodology

The project was developed using an iterative waterfall methodology with the following phases:

1. **Requirements Analysis:** Functional and non-functional requirements were identified based on a thorough literature survey of existing 3D reconstruction approaches and user needs. The requirements were documented in a Software Requirements Specification (SRS).

2. **System Design:** The overall system architecture was designed, including the pipeline stage orchestrator, database schema, API routes, and frontend component hierarchy. A modular design was adopted to allow independent development and testing of each pipeline stage.

3. **Model Selection and Integration:** Each AI model (Florence-2, GroundingDINO, SAM2.1, rembg, Hunyuan3D-2) was evaluated for suitability, and integration wrappers were developed with standardized input/output interfaces. A sequential memory management layer was implemented to load, execute, and unload models one at a time.

4. **Backend Development:** The FastAPI backend was implemented with route handlers, controllers, and the pipeline orchestrator. Authentication middleware was built using Supabase Auth and JWT validation. Database operations were implemented using the Supabase Python client.

5. **Frontend Development:** The Next.js web application was built with pages for upload, processing status, results viewing, history, profile, and authentication. React Three Fiber was used for 3D visualization. Real-time pipeline progress was implemented via periodic status polling.

6. **Testing:** Unit tests were written for individual pipeline modules using PyTest. Integration tests verified stage-to-stage communication and end-to-end API behaviour. Performance benchmarks measured pipeline execution time and VRAM usage. Frontend tests were implemented using Playwright.

7. **Optimization:** Pipeline stages were profiled and optimized. VRAM management was refined to eliminate memory leaks. Image downscaling and lazy model loading were added for low-memory environments.

8. **Deployment:** The system was containerized using Docker Compose with separate frontend and backend services. Environment-based configuration was implemented for development and production deployments.
