
# Requirements Specification

## 1. Introduction

This document defines the functional and non-functional requirements for the Automated Single-Image to 3D Asset and Point Cloud Generation System.

The objective of the system is to automatically generate a textured 3D model and segmented point cloud from a single input image using modern AI foundation models, with authenticated user access and persistent job history.

---

# 2. Functional Requirements

## FR-01 Image Upload

The system shall allow users to upload a single RGB image.

Supported formats:

- JPG
- JPEG
- PNG
- WEBP
- BMP

Maximum image size:

- 25 MB

---

## FR-02 Image Validation

The system shall validate:

- Image format
- Image size
- Corrupted files
- Unsupported extensions

Invalid images shall be rejected with an appropriate error message.

---

## FR-03 Image Analysis

The system shall compute:

- Mean brightness
- Contrast
- Resolution
- Color channels

---

## FR-04 Adaptive Enhancement

If the image is classified as:

- Dark
- Low Contrast

The system shall automatically apply:

- CLAHE (Contrast Limited Adaptive Histogram Equalization)

Normal images shall bypass enhancement.

---

## FR-05 Automatic Caption Generation

The system shall automatically generate a caption using Florence-2.

Example:

"a black ceramic mug"

No manual prompt shall be required.

---

## FR-06 Prompt Generation

The generated caption shall automatically be converted into a GroundingDINO-compatible prompt.

Example:

black . ceramic . mug

---

## FR-07 Zero-Shot Object Detection

GroundingDINO shall detect the primary object.

Detection strategy:

Pass 1

Confidence = 0.20

↓

Pass 2

Enhanced Image

↓

Pass 3

Confidence = 0.15

↓

Pass 4

Confidence = 0.10

---

## FR-08 Part Detection

Florence-2 shall detect object parts.

Example:

Mug

- Body
- Handle

Chair

- Seat
- Legs
- Backrest

---

## FR-09 Instance Segmentation

SAM2.1 shall generate:

- Pixel-accurate masks
- Binary masks
- Best IoU mask selection

---

## FR-10 Background Removal

The system shall remove the background using:

- rembg (ONNX Runtime)
- SAM2.1 mask applied to refine alpha channel

Output:

RGBA Image

Transparent Background

---

## FR-11 3D Mesh Generation

The system shall generate:

- Watertight Mesh

using

Hunyuan3D-2

---

## FR-12 Texture Generation

The system shall generate:

- PBR Texture

Output format:

GLB

---

## FR-13 Mesh Visualization

The generated mesh shall be viewable inside:

- Open3D
- Browser (Three.js / React Three Fiber)

---

## FR-14 Point Cloud Generation

The mesh shall be converted into a point cloud using:

Poisson Disk Sampling

---

## FR-15 Surface Normal Estimation

The generated point cloud shall include:

- Normals
- Normal Orientation

---

## FR-16 Point Cloud Segmentation

The system shall segment the point cloud using:

DBSCAN

Outputs:

- Cluster Labels
- Colored Point Cloud

---

## FR-17 Export

Users shall be able to download:

- GLB
- PLY
- PNG
- JSON (metadata always generated)

---

## FR-18 User Authentication

The system shall provide user authentication via Supabase Auth.

Requirements:

- Email/password signup and login
- JWT-based session management
- Bearer token authorization header for API calls
- Protected frontend routes redirect unauthenticated users
- Local development mock user fallback

---

## FR-19 Supabase Database Integration

The system shall persist pipeline execution records to Supabase PostgreSQL.

Tables:

- **profiles** — Synced automatically from `auth.users`
- **jobs** — Pipeline execution with status, timing, ownership
- **artifacts** — File metadata for each generated output

The system shall fall back to local JSON file storage when Supabase is unavailable.

---

## FR-20 Job History

The system shall allow authenticated users to:

- View paginated job history
- Filter by filename and status
- Sort by newest or oldest
- View job details and artifact listing
- Delete (soft delete) jobs

---

# 3. Non-Functional Requirements

## Performance

Complete pipeline:

Target:

≤ 4 Minutes

GPU:

CUDA Enabled

---

## Reliability

The system shall:

- Recover from detection failures
- Retry detection
- Prevent crashes
- Fall back to local storage when database is unavailable

---

## Scalability

The system shall support:

- Multiple object categories
- Different image resolutions
- Future AI models

---

## Usability

The application shall provide:

- Simple UI
- Progress indicator
- Download buttons
- Login / signup flow
- History dashboard

---

## Maintainability

The project shall use:

- Modular architecture
- Independent AI modules
- Clean folder structure

---

## Portability

Supported Platforms:

- Windows
- Linux

---

## Security

The system shall:

- Validate uploaded images
- Reject malicious files
- Limit upload size
- Authenticate API requests via JWT
- Enforce per-user data isolation (RLS policies)

---

# 4. Hardware Requirements

Minimum

CPU

Intel Core i7

RAM

16 GB

GPU

NVIDIA RTX 3050

VRAM

4 GB

Storage

50 GB

Recommended

RAM

32 GB

GPU

RTX 4070+

VRAM

12 GB+

---

# 5. Software Requirements

Operating System

Windows 11
Ubuntu 22+

Python

3.11+

CUDA

12.1+

Libraries

PyTorch

OpenCV

Open3D

Transformers

Pillow

NumPy

rembg

ONNX Runtime

FastAPI

Uvicorn

Supabase

pydantic-settings

PyYAML

python-multipart

httpx

python-jose

Three.js

React

Next.js

Tailwind CSS

React Three Fiber

Drei

lucide-react

@supabase/supabase-js

---

# 6. AI Models

Florence-2

GroundingDINO

SAM2.1

rembg (ONNX Runtime)

Hunyuan3D-2

---

# 7. Expected Outputs

Generated Files

✓ Detection Image

✓ Segmentation Image

✓ RGBA Image

✓ GLB Model

✓ Point Cloud

✓ Segmented Point Cloud

✓ JSON Metadata

---

# 8. Success Criteria

The project shall be considered successful if it:

✓ Authenticates users

✓ Detects the object

✓ Generates segmentation

✓ Removes background

✓ Produces textured GLB

✓ Produces point cloud

✓ Segments the point cloud

✓ Exports all outputs successfully

✓ Persists job history
