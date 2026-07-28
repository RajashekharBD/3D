# Automated Single-Image to 3D Asset and Point Cloud Generation System

A production-grade, full-stack AI platform that transforms a single 2D RGB image into a fully textured 3D mesh (`.GLB`) and semantically segmented point cloud (`.PLY`) in under 4 minutes. 

Powered by **Florence-2**, **GroundingDINO**, **SAM 2.1**, **rembg (ONNX)**, **Hunyuan3D-2**, **Open3D**, **FastAPI**, and **Next.js 14**.

---

## 📌 Table of Contents
1. [Project Overview & Key Features](#-project-overview--key-features)
2. [Hardware & Software Requirements](#-hardware--software-requirements)
3. [AI Models & Pipeline Architecture](#-ai-models--pipeline-architecture)
4. [Step-by-Step Installation Guide](#-step-by-step-installation-guide)
5. [AI Model Checkpoints & Setup](#-ai-model-checkpoints--setup)
6. [Environment Variables Configuration](#-environment-variables-configuration)
7. [How to Start the Project](#-how-to-start-the-project)
8. [Project Directory Structure](#-project-directory-structure)
9. [Testing & Verification](#-testing--verification)
10. [Troubleshooting & FAQs](#-troubleshooting--faqs)

---

## 🌟 Project Overview & Key Features

| Feature | Details |
| :--- | :--- |
| **Prompt-Free Execution** | Eliminates manual text prompt engineering by using **Florence-2** to auto-caption uploaded images. |
| **Multi-Pass Detection** | **GroundingDINO** detects object bounding boxes with a 4-pass CLAHE/confidence threshold fallback strategy. |
| **Precision Masking** | **SAM 2.1** & **rembg (ONNX)** extract pixel-perfect transparent RGBA cutouts free of background noise. |
| **3D Mesh Generation** | **Hunyuan3D-2** diffusion model synthesizes watertight 3D geometry & PBR textures exported in `.GLB` format. |
| **Point Cloud Clustering** | **Open3D** samples 100,000 surface points (Poisson Disk) and segments them via density-based **DBSCAN**. |
| **Interactive 3D Viewer** | Next.js 14 WebGL canvas powered by **Three.js** with 360° controls, quick preview modals, and wireframe toggle. |
| **User Persistence & Security**| **Supabase Auth** (JWT) and **Supabase PostgreSQL** database with Row-Level Security (RLS). |

---

## 💻 Hardware & Software Requirements

### Hardware Specifications
* **CPU:** Intel Core i7 / AMD Ryzen 7 (11th Gen+ recommended).
* **GPU:** NVIDIA GPU with CUDA support (**Minimum 8 GB VRAM**, 12 GB+ VRAM recommended e.g. RTX 3080/4070/T4).
* **RAM:** 16 GB Minimum (32 GB recommended for loading heavy PyTorch checkpoints).
* **Storage:** 50 GB available SSD space (for PyTorch models, Hugging Face cache, and generated 3D assets).

### Software Requirements
* **OS:** Windows 10/11 64-bit or Linux (Ubuntu 22.04 LTS).
* **Runtimes:** Python 3.10+, Node.js v18.0+, npm v9.0+.
* **CUDA:** NVIDIA CUDA Toolkit 11.8 or 12.1 + cuDNN v8.x.

---

## ⚙️ AI Models & Pipeline Architecture

```
Raw Image Upload ➔ CLAHE Contrast Enhancement ➔ Florence-2 Auto Captioning
                       ↓
GroundingDINO Box Detection ➔ SAM 2.1 Masking ➔ rembg RGBA Cutout
                       ↓
Hunyuan3D-2 Geometry & Texture Diffusion ➔ .GLB Textured Mesh
                       ↓
Open3D Poisson 100k Point Cloud Sampling ➔ DBSCAN Clustering ➔ .PLY Point Cloud
```

---

## 🛠️ Step-by-Step Installation Guide

### 1. Clone the Repository
```bash
git clone https://github.com/RajashekharBD/3D.git
cd 3D
```

### 2. Set Up Python Virtual Environment (Backend)
```bash
# On Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\activate

# On Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install PyTorch with CUDA Support
```bash
# Install PyTorch with CUDA 11.8/12.1 support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 4. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 5. Install SAM 2.1 & Additional Packages
```bash
pip install git+https://github.com/facebookresearch/sam2.git
pip install diffusers transformers accelerate trimesh open3d rembg onnxruntime
```

### 6. Install Frontend Node Dependencies
```bash
cd frontend
npm install
cd ..
```

---

## 🤖 AI Model Checkpoints & Setup

The system automatically downloads required weights from **Hugging Face Hub** on the first run and caches them locally:

* **Florence-2:** `microsoft/Florence-2-large` (Auto-downloaded via `transformers`).
* **GroundingDINO:** `IDEA-Research/grounding-dino-base` (Auto-downloaded via `transformers`).
* **SAM 2.1:** `facebook/sam2.1-hiera-large` (Auto-downloaded via PyTorch / SAM 2).
* **rembg:** `u2net` (Auto-downloaded on first run via `rembg`).
* **Hunyuan3D-2:** `Tencent/Hunyuan3D-2` (Stage-1 geometry & Stage-2 texture diffusion pipelines loaded via `diffusers`).

> 💡 **Tip:** Model checkpoints are cached in `~/.cache/huggingface/` or `ai_models/`. Make sure you have an active internet connection on the first run.

---

## 🔑 Environment Variables Configuration

### Root `.env` (Backend Configuration)
Create a `.env` file in the root directory `c:\Personal\3D\.env`:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development

# Storage Directories
OUTPUT_DIR=outputs
LOG_LEVEL=INFO

# Supabase Credentials (Optional for local fallback mode)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key

# Memory Optimization Settings
CUDA_VISIBLE_DEVICES=0
ENABLE_CPU_OFFLOAD=true
```

### Frontend `.env.local`
Create a `.env.local` file inside `frontend/.env.local`:

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key

NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

---

## 🚀 How to Start the Project (Recommended Local Setup)

We recommend running the system directly using your local Python virtual environment and Node.js. Start the **FastAPI Backend** and **Next.js Frontend** in two separate terminals:

### Terminal 1: Start FastAPI Backend
```bash
# Activate virtual environment and start FastAPI backend
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
* Backend Swagger API Docs: `http://localhost:8000/docs`
* Health Check Endpoint: `http://localhost:8000/api/v1/health`

### Terminal 2: Start Next.js Frontend
```bash
cd frontend
npm run dev
```
* Access the Web Application at: `http://localhost:3000`

---

## 🐳 Optional: Running with Docker Compose (Production Servers Only)

If deploying to a remote Linux cloud server with NVIDIA Container Toolkit installed:

```bash
docker-compose up --build
```

---

## 📂 Project Directory Structure

```
3D/
├── backend/                  # FastAPI Backend Application
│   ├── app/
│   │   ├── api/              # HTTP Endpoints (/upload, /download, /history)
│   │   ├── controllers/      # Request handlers & logic
│   │   ├── core/             # Settings, database, and auth security
│   │   ├── pipeline/         # 11-Stage AI pipeline modules
│   │   ├── services/         # Image & 3D processing services
│   │   └── utils/            # Artifacts manager & logging
│   └── main.py               # FastAPI entry point
├── frontend/                 # Next.js 14 Web Application
│   ├── app/                  # App Router (/upload, /history, /profile, /results)
│   ├── components/           # UI Components & ThreeViewer WebGL Canvas
│   ├── context/              # Auth & Theme context providers
│   └── package.json
├── docs/                     # SRS, System Architecture, & Report Documentation
├── generate_pdf.py           # Script to compile 17-Page Capstone PDF Report
├── ESA_Capstone_Project_Report.pdf # Generated PDF Report
├── outputs/                  # Local 3D assets storage (.GLB, .PLY, .PNG)
├── requirements.txt          # Python dependencies
├── docker-compose.yml
└── README.md
```

---

## 🧪 Testing & Verification

Run backend unit tests and benchmarks:

```bash
# Run pytest test suite
pytest

# Run test coverage report
pytest --cov=backend

# Run frontend Playwright UI end-to-end tests
cd frontend
npx playwright test
```

---

## ❓ Troubleshooting & FAQs

#### 1. Out of Memory (OOM) GPU Error
If your GPU runs out of VRAM during Hunyuan3D-2 generation:
* Ensure `ENABLE_CPU_OFFLOAD=true` is set in `.env`.
* The system automatically enables `sequential_cpu_offload`, `attention_slicing`, and `vae_tiling`.

#### 2. "Failed to Fetch" or Supabase SSL Error in Browser
If your browser displays `net::ERR_CERT_AUTHORITY_INVALID` when logging in:
1. Open a new tab and visit `https://your-supabase-project.supabase.co`.
2. Click **Advanced ➔ Proceed to site (unsafe)** to establish browser SSL trust.
3. Return to `http://localhost:3000` and retry login.

---

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.
