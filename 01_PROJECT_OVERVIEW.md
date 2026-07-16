
# Automated Single-Image to 3D Asset and Point Cloud Generation System

## Overview

The Automated Single-Image to 3D Asset and Point Cloud Generation System is an AI-powered application that automatically converts a single RGB image into a high-quality textured 3D model and a segmented point cloud without requiring manual prompt engineering or multiple input images.

The system integrates state-of-the-art computer vision and generative AI models into one automated pipeline capable of performing object detection, instance segmentation, background removal, 3D reconstruction, point cloud generation, and semantic segmentation.

The generated outputs are suitable for:

- Augmented Reality (AR)
- Virtual Reality (VR)
- WebXR
- Robotics
- Digital Twin Applications
- Product Visualization
- Industrial Inspection
- E-commerce

---

# Objectives

The project aims to:

- Detect the primary object from a single image.
- Automatically generate captions without user prompts.
- Detect object parts.
- Produce pixel-accurate segmentation.
- Remove image background.
- Generate a textured 3D mesh.
- Convert the mesh into a dense point cloud.
- Segment the point cloud into meaningful clusters.
- Export standard 3D formats.

---

# Core Features

- Single image upload
- Automatic image enhancement
- AI caption generation
- Zero-shot object detection
- Part-level detection
- Pixel-accurate segmentation
- Automatic background removal
- High-quality textured GLB generation
- Mesh visualization
- Point cloud generation
- DBSCAN clustering
- Downloadable outputs

---

# Input

Supported formats

- JPG
- JPEG
- PNG
- WEBP
- BMP

---

# Outputs

Generated Files

- Annotated Detection Image
- Segmented Image
- RGBA Image
- GLB Mesh
- Point Cloud (.PLY)
- Segmented Point Cloud (.PLY)

---

# AI Models

- Florence-2
- GroundingDINO
- SAM2.1
- rembg
- Hunyuan3D-2

---

# Point Cloud Processing

- Open3D
- Poisson Disk Sampling
- DBSCAN
- Normal Estimation

---

# End-to-End Pipeline

Input Image
    ↓
Image Analysis
    ↓
CLAHE Enhancement
    ↓
Florence-2 Caption Generation
    ↓
GroundingDINO Detection
    ↓
Florence-2 Part Detection
    ↓
SAM2.1 Segmentation
    ↓
Background Removal
    ↓
Hunyuan3D-2 Shape Generation
    ↓
Texture Synthesis
    ↓
GLB Export
    ↓
Point Cloud Generation
    ↓
DBSCAN Segmentation
    ↓
PLY Export

---

# Expected Runtime

GPU:

- NVIDIA GPU
- CUDA Enabled

Expected execution:

Approximately 3–4 minutes for complete pipeline execution depending on GPU capability.

---

# Applications

- AR Product Viewer
- VR Asset Generation
- Digital Museum
- Robotics
- Industrial Inspection
- E-commerce
- CAD Prototype Generation
- Education

---

# Project Goals

- Fully automated
- Prompt-free
- Modular architecture
- Production ready
- Easily extensible
- Cross-platform
