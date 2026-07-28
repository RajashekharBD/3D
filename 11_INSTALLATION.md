
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
- Supabase Setup
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
- Supabase CLI (for database migrations)

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

The following models are automatically downloaded from Hugging Face during first execution:

- Florence-2
- GroundingDINO
- SAM2.1
- Hunyuan3D-2

Models are cached locally via Hugging Face `transformers` on first use. No separate download script is needed.

---

# Supabase Setup

## Create Supabase Project

1. Go to https://supabase.com and sign in.
2. Click **New Project** and enter project details.
3. Wait for database provisioning to complete.

## Get API Credentials

From the Supabase dashboard (Project Settings → API):

- **Project URL** — used as `SUPABASE_URL`
- **anon public key** — used as `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- **service_role key** — used as `SUPABASE_SERVICE_ROLE_KEY`

From Project Settings → API → JWT Settings:

- **JWT Secret** — used as `SUPABASE_JWT_SECRET`

## Run Migrations

```bash
supabase link --project-ref your-project-ref

supabase migration up
```

---

# Configure Environment

## Backend (.env)

Copy `.env.example` to `.env` in the project root and update values.

```
APP_NAME=SingleImage3D

APP_ENV=development

HOST=0.0.0.0

PORT=8000

LOG_LEVEL=INFO

CUDA_DEVICE=0

OUTPUT_DIR=outputs

TEMP_DIR=data/temp

MAX_UPLOAD_SIZE_MB=25

DELETE_TEMP_FILES=true

SUPABASE_URL=https://your-project.supabase.co

SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

SUPABASE_JWT_SECRET=your-jwt-secret
```

## Frontend (.env.local)

Create `frontend/.env.local`:

```
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co

NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key

NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
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

supabase/
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

Supabase

Connected

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

Models download automatically on first use via Hugging Face `transformers`.

---

## Supabase Connection Failed

Check

- SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY values in .env
- NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY in frontend/.env.local
- Project is active in Supabase dashboard
- Network access (no firewall blocking)

The backend falls back to local/mock mode if Supabase is unavailable.

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
- Supabase Project Created
- Migrations Applied
- Environment Variables Configured
- Backend Running
- Frontend Running
- GPU Verified
- API Verified

Installation is complete when all items above are successful.
