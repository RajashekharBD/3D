# KLE Society's

# KLE Technological University, Hubballi

## Department Of MCA

### MCA IV Semester

# CHAPTER – 10

# APPENDIX

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

## 10.1 Appendix A — Glossary

| Term                              | Definition                                                                                                                               |
| :-------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| **3D Reconstruction**       | The process of inferring 3D surface geometry, volume, and texture from one or more 2D image inputs.                                      |
| **Point Cloud**             | A set of data points defined by$(X, Y, Z)$ spatial coordinates representing the external surface geometry of an object.                |
| **Poisson Disk Sampling**   | A uniform surface sampling technique that maintains a minimum distance between sample points to avoid clustering.                        |
| **.GLB**                    | GL Transmission Format (Binary) — A compact binary file format containing 3D mesh geometry, textures, and material shaders.             |
| **.PLY**                    | Polygon File Format — A standard format for storing 3D point cloud data, surface colors, and vertex normal vectors.                     |
| **SAM**                     | Segment Anything Model — A foundation vision model trained by Meta AI for zero-shot object isolation and alpha matting.                 |
| **Triplane Representation** | An implicit 3D neural feature representation that projects 3D spatial features onto three orthogonal 2D feature planes ($XY, XZ, YZ$). |
| **WebGL**                   | Web Graphics Library — A cross-platform JavaScript API for rendering interactive 3D graphics in modern web browsers without plugins.    |
| **JWT**                     | JSON Web Token — A compact, URL-safe security token used to authenticate users and authorize API requests securely.                     |
| **RLS**                     | Row Level Security — A database policy feature in PostgreSQL / Supabase restricting data access strictly to authorized users.           |
| **FPS**                     | Frames Per Second — A performance metric measuring 3D viewport rendering speed, targeting 60 FPS for fluid interaction.                 |
| **VRAM**                    | Video Random Access Memory — Dedicated high-speed GPU memory utilized for deep learning tensor execution and model weights.             |

---

## 10.2 Appendix B — Description on Technology Used

**Generative 3D Mesh Synthesis Engine (Hunyuan3D-2)**
Hunyuan3D-2 is a state-of-the-art feed-forward 3D generative model developed by Tencent. It utilizes a dual-stage architecture—a triplane diffusion generator followed by a mesh synthesizer—to convert 2D RGB features into watertight, textured 3D polygon meshes (`.GLB`) in under 15 seconds.

**Meta Segment Anything Model (SAM 2.1)**
Meta AI's Segment Anything Model (SAM 2.1) provides zero-shot image segmentation. In this project, SAM isolates the primary foreground subject from raw RGB images, removing background clutter and generating a clean transparent RGBA cutout with alpha matting.

**3D Graphics & Point Cloud Processing Library (Open3D)**
Open3D is an open-source library for 3D data processing. It is responsible for converting 3D polygon meshes into 10,000 uniform Poisson-disk surface point samples and computing $k$-nearest neighbor ($k$-NN) surface normal vectors for point cloud analysis.

**Modern Web Application Framework (Next.js 15 & React 19)**
Next.js 15 is a modern React web framework providing server-side rendering, client-side dynamic routing via the App Router, and fast hot-module reloading powered by Turbopack. It serves as the user-facing web dashboard.	

**Declarative 3D WebGL Canvas Engine (React Three Fiber & Three.js)**
React Three Fiber is a declarative React wrapper around Three.js. It powers the interactive 3D WebGL viewport canvas, providing real-time 60 FPS rendering, lighting, shading, and mouse orbit controls (pan, zoom, rotate).

---

## 10.3 Appendix C — Explanation on Tools

| Tool | Purpose |
| :--- | :--- |
| **PyTorch & CUDA 12.1** | Deep learning framework and GPU compute architecture used for executing SAM and Hunyuan3D model weights. |
| **Uvicorn ASGI Server** | High-performance asynchronous web server hosting the FastAPI backend application. |
| **Node.js & npm** | JavaScript runtime environment and package manager for executing Next.js build scripts and managing frontend dependencies. |
| **Tailwind CSS v4** | Utility-first CSS framework used for building the responsive glassmorphism UI design system. |
| **Git / GitHub** | Version control system for source code management, branch tracking, and repository collaboration. |
| **VS Code & Antigravity IDE** | Primary development environments for code editing, TypeScript type-checking, and automated linting. |
| **Postman / Swagger UI** | Interactive web interface and API testing tools used for verifying RESTful endpoints and OpenAPI schemas. |
