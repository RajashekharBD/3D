
# Technology Stack

## Overview

The Automated Single-Image to 3D Asset and Point Cloud Generation System is built using a modern AI and computer vision stack. Every technology has been selected based on performance, scalability, compatibility, and long-term maintainability.

---

# System Architecture

Frontend
        │
        ▼
REST API (FastAPI)
        │
        ▼
AI Processing Pipeline
        │
        ▼
3D Processing
        │
        ▼
Output Generation

---

# Frontend

## Framework

Next.js 15.5

Purpose

- Modern React framework
- Fast routing
- Server-side rendering
- Production-ready

Version

15.5

---

## UI Library

React 19.1

Purpose

- Component-based UI
- State management
- Interactive interface

---

## Styling

Tailwind CSS 4

Purpose

- Responsive UI
- Utility-first styling
- Faster development

---

## 3D Rendering

Three.js 0.185

Purpose

- Display generated GLB models
- Interactive camera
- Lighting
- Animation

---

## React Three Fiber 9.6

Purpose

- React wrapper for Three.js
- Simplifies 3D rendering

---

## Drei 10.7

Purpose

- Orbit Controls
- Environment
- Helpers
- Camera controls

---

## UI Icons

lucide-react 1.24

Purpose

- Icon components for UI

---

# Backend

## Framework

FastAPI 0.110+

Purpose

- REST API
- High performance
- Async support
- Automatic API documentation

---

## ASGI Server

Uvicorn 0.28+

Purpose

- Runs FastAPI server
- High-speed asynchronous server

---

# Programming Language

Python

Version

3.11+

Purpose

- AI
- Deep Learning
- Computer Vision
- Image Processing
- 3D Processing

---

# Authentication & Database

## Supabase

Purpose

- User authentication (Auth)
- PostgreSQL database
- Row Level Security
- Session management

Backend Package

supabase 2.4+ (Python)
@supabase/supabase-js 2.43+ (Frontend)

---

# AI Models

## Florence-2

Purpose

- Automatic Caption Generation
- Part Detection

Input

Image

Output

Caption
Object Parts

---

## GroundingDINO

Purpose

- Zero-shot Object Detection

Input

Image
Caption Prompt

Output

Bounding Boxes

---

## SAM2.1

Purpose

- Instance Segmentation

Input

Bounding Boxes

Output

Binary Masks

---

## rembg

Purpose

- Background Removal

Backend

ONNX Runtime

Output

RGBA Image (refined with SAM2.1 mask)

---

## Hunyuan3D-2

Purpose

- Shape Generation
- Texture Generation

Output

GLB

---

# Deep Learning Framework

PyTorch

Purpose

- Model Loading
- GPU Inference
- Tensor Operations

CUDA Support

Yes

---

# Hugging Face

Purpose

- Download AI Models
- Model Management
- Transformers

Models Used

- Florence-2
- GroundingDINO
- SAM2.1
- Hunyuan3D-2

---

# Image Processing

## OpenCV 4.9+

Purpose

- CLAHE
- Image Analysis
- Image Enhancement
- Image Conversion

---

## Pillow 10.2+

Purpose

- Image Loading
- Image Saving
- RGB Conversion

---

## NumPy 1.26+

Purpose

- Numerical Operations
- Matrix Manipulation
- Image Arrays

---

# 3D Processing

## Open3D 0.18+

Purpose

- Mesh Viewer
- Point Cloud Generation
- Point Cloud Visualization
- Normal Estimation

---

# Point Cloud Processing

Algorithm

Poisson Disk Sampling

Purpose

Generate Uniform Point Cloud

---

Algorithm

DBSCAN

Purpose

Point Cloud Segmentation

---

# API Communication

Protocol

REST API

Data Format

JSON

Image Upload

Multipart Form Data

---

# Output Formats

Images

PNG

JPEG

---

3D

GLB

---

Point Cloud

PLY

---

Metadata

JSON

---

# Configuration & Utilities

## pydantic-settings 2.2+

Purpose

- Environment variable loading
- Settings management

---

## PyYAML 6.0+

Purpose

- YAML config file loading

---

## python-multipart 0.0.9+

Purpose

- Multipart file upload parsing

---

## httpx

Purpose

- Async HTTP client
- Supabase JWT verification

---

## python-jose 3.3+

Purpose

- JWT token handling

---

# Development Tools

## Visual Studio Code

Purpose

Code Development

---

## Git

Purpose

Version Control

---

## GitHub

Purpose

Source Code Repository

---

# Operating System

Development

Windows 11

Deployment

Ubuntu 22.04+

---

# Hardware

Minimum

CPU

Intel Core i7

RAM

16 GB

GPU

RTX 3050

VRAM

4 GB

---

Recommended

CPU

Intel Core i7 / i9

RAM

32 GB

GPU

RTX 4070+

VRAM

12 GB+

---

# Why These Technologies?

| Technology               | Purpose                    | Reason                            |
| ------------------------ | -------------------------- | --------------------------------- |
| Next.js                  | Frontend                   | Modern production framework        |
| React                    | UI                         | Component-based architecture       |
| Tailwind CSS             | Styling                    | Fast responsive UI                 |
| FastAPI                  | Backend                    | High-performance REST API          |
| PyTorch                  | AI                         | Industry-standard deep learning    |
| Florence-2               | Captioning                 | Automatic prompt generation        |
| GroundingDINO            | Detection                  | Zero-shot object detection         |
| SAM2.1                   | Segmentation               | Accurate object masks              |
| rembg                    | Background Removal         | Clean RGBA object extraction       |
| Hunyuan3D-2              | 3D Generation              | High-quality textured mesh         |
| OpenCV                   | Image Processing           | CLAHE and image enhancement        |
| Open3D                   | 3D Processing              | Mesh and point cloud handling      |
| Three.js                 | 3D Viewer                  | Browser-based visualization        |
| React Three Fiber        | 3D React Wrapper           | Declarative 3D scenes in React     |
| Drei                     | 3D Helpers                 | Orbit controls, environment        |
| Supabase                 | Auth & Database            | Authentication and PostgreSQL      |
| DBSCAN                   | Segmentation               | Point cloud clustering             |
| lucide-react             | Icons                      | Consistent UI icon set             |

---

# Technology Flow

Image
   │
   ▼
OpenCV
   │
   ▼
Florence-2
   │
   ▼
GroundingDINO
   │
   ▼
SAM2.1
   │
   ▼
rembg (with SAM2.1 mask)
   │
   ▼
Hunyuan3D-2
   │
   ▼
Open3D
   │
   ▼
DBSCAN
   │
   ▼
GLB + PLY + JSON Output
