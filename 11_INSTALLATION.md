
# Installation Guide

## Overview

This document describes how to set up the complete development environment for the Automated Single-Image to 3D Asset and Point Cloud Generation System.

The installation process covers:

- System Requirements
- Software Installation
- Python Environment
- CUDA Setup
- AI Model Download
- Backend Setup
- Frontend Setup
- Verification

---

# System Requirements

## Minimum

CPU

Intel Core i7 (12th Gen or equivalent)

RAM

16 GB

GPU

NVIDIA RTX 3050

VRAM

4 GB

Storage

100 GB Free

Operating System

Windows 11 (64-bit)

---

## Recommended

CPU

Intel Core i7 / i9

RAM

32 GB

GPU

RTX 4070 or above

VRAM

12 GB+

Storage

200 GB SSD

---

# Required Software

Install the following software before proceeding.

- Git
- Python 3.11
- Node.js LTS
- Visual Studio Code
- NVIDIA Driver (latest)
- CUDA Toolkit 12.1
- cuDNN (compatible with CUDA 12.1)

---

# Clone Repository

```bash
git clone https://github.com/yourusername/single-image-3d-system.git

cd single-image-3d-system
```

---

# Create Python Environment

Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

Linux

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

# Upgrade Pip

```bash
python -m pip install --upgrade pip
```

---

# Install Backend Dependencies

```bash
pip install -r backend/requirements.txt
```

---

# Install Frontend Dependencies

```bash
cd frontend

npm install
```

---

# Install PyTorch

CUDA 12.1

```bash
pip install torch torchvision torchaudio
```

Verify

```bash
python -c "import torch;print(torch.cuda.is_available())"
```

Expected

```
True
```

---

# Download AI Models

The following models are automatically downloaded during first execution:

- Florence-2
- GroundingDINO
- SAM2.1
- Hunyuan3D-2

Alternatively

```bash
python scripts/download_models.py
```

---

# Verify GPU

Run

```bash
nvidia-smi
```

Check

- Driver Installed
- CUDA Version
- GPU Detected
- Available VRAM

---

# Project Structure Check

```
backend/

frontend/

ai_models/

configs/

outputs/

scripts/

tests/

docs/
```

---

# Configure Environment

Copy

```
.env.example
```

to

```
.env
```

Update values as required.

Example

```
CUDA_DEVICE=0

OUTPUT_DIR=outputs

TEMP_DIR=data/temp

LOG_LEVEL=INFO
```

---

# Start Backend

```bash
cd backend

uvicorn app.main:app --reload
```

Expected

```
http://localhost:8000
```

---

# Start Frontend

```bash
cd frontend

npm run dev
```

Expected

```
http://localhost:3000
```

---

# Verify Installation

Open browser

```
http://localhost:3000
```

Expected

Home Page

↓

Upload Page

↓

Image Upload

↓

Pipeline Ready

---

# Run Health Check

```
GET

/api/v1/health
```

Expected Response

```json
{
    "status":"healthy"
}
```

---

# Test GPU

```python
import torch

print(torch.cuda.is_available())

print(torch.cuda.get_device_name(0))
```

---

# Test OpenCV

```python
import cv2

print(cv2.__version__)
```

---

# Test Open3D

```python
import open3d as o3d

print(o3d.__version__)
```

---

# Test Transformers

```python
from transformers import AutoProcessor

print("OK")
```

---

# Test FastAPI

Open

```
http://localhost:8000/docs
```

Swagger UI should appear.

---

# Expected Installation Result

Backend

Running

Frontend

Running

CUDA

Available

PyTorch

GPU Enabled

OpenCV

Working

Open3D

Working

Transformers

Working

API

Accessible

---

# Troubleshooting

## CUDA Not Detected

Check

- NVIDIA Driver
- CUDA Toolkit
- PyTorch CUDA Version

---

## Out of Memory

Possible Solutions

- Close other GPU applications
- Reduce image resolution
- Process one image at a time
- Enable CPU offloading for Hunyuan3D-2 if supported

---

## Model Download Failed

Check

- Internet Connection
- Hugging Face Access
- Available Disk Space

Retry

```bash
python scripts/download_models.py
```

---

# Installation Checklist

- Python Installed
- Node.js Installed
- Git Installed
- CUDA Installed
- NVIDIA Driver Updated
- Virtual Environment Created
- Backend Dependencies Installed
- Frontend Dependencies Installed
- AI Models Downloaded
- Backend Running
- Frontend Running
- GPU Verified
- API Verified

Installation is complete when all items above are successful.
