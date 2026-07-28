
# Frontend Architecture

## Overview

The frontend provides a clean, responsive interface for users to upload an image, monitor AI processing, preview outputs, visualize the generated 3D model, and download all generated assets.

Built with:
- Next.js 15 (App Router)
- React 19
- TypeScript
- Tailwind CSS
- React Three Fiber + Drei + Three.js
- Supabase Auth (client-side)

---

# User Workflow

```
Home (/)
  │
  ▼
Login / Signup (/login, /signup)
  │
  ▼
Upload Image (/upload)
  │
  ▼
Processing Progress (/processing/[jobId])
  │
  ▼
Results + 3D Viewer (/results/[jobId])
  │
  ▼
Download Artifacts (inline in results page)
  │
  ▼
History (/history) — browse past jobs
  │
  ▼
Profile (/profile) — stats & account info
```

---

# Routes

| Route | Page | Auth |
|-------|------|------|
| `/` | Landing page (hero + features) | No |
| `/upload` | Image upload (drag & drop) | Protected |
| `/processing/[jobId]` | Pipeline progress tracker | Protected |
| `/results/[jobId]` | Reconstruction results + 3D viewer | Protected |
| `/login` | Login form | No |
| `/signup` | Registration form | No |
| `/forgot-password` | Password reset | No |
| `/history` | Paginated job history grid | Protected |
| `/profile` | User profile + statistics | Protected |
| `/viewer` | Generic 3D viewer (redirect to upload) | No |
| `/download` | Generic download page (redirect to upload) | No |

---

# Folder Structure

```
frontend/
  app/
    page.tsx                     → Landing page (/)
    layout.tsx                   → Root layout (Navbar + AuthProvider + Footer)
    upload/page.tsx              → Image upload (/upload)
    processing/[jobId]/page.tsx  → Progress tracker (/processing/[jobId])
    results/[jobId]/page.tsx     → Results + 3D viewer (/results/[jobId])
    login/page.tsx               → Login form (/login)
    signup/page.tsx              → Signup form (/signup)
    forgot-password/page.tsx     → Forgot password (/forgot-password)
    history/page.tsx             → Job history (/history)
    profile/page.tsx             → User profile (/profile)
    viewer/page.tsx              → Viewer redirect (/viewer)
    download/page.tsx            → Download redirect (/download)
  components/
    Auth/
      LoginForm.tsx
      SignupForm.tsx
      ForgotPasswordForm.tsx
      ProtectedRoute.tsx
    Download/
      DownloadPanel.tsx          → Artifact download buttons
    Footer/
      Footer.tsx
    History/
      HistoryGrid.tsx            → Paginated searchable grid
      HistoryCard.tsx            → Individual job card
      SearchBar.tsx
      SortMenu.tsx
    Navbar/
      Navbar.tsx                 → Nav with auth-aware links
    Profile/
      ProfileCard.tsx            → User info card
      StatisticsCard.tsx         → Usage stats
    Progress/
      ProgressTracker.tsx        → Live pipeline progress + phase list
    ThreeViewer.tsx              → GLB/PLY viewer (R3F)
  context/
    AuthContext.tsx              → Supabase auth state provider
  utils/
    supabaseClient.ts           → Supabase client singleton
```

---

# Key Components

## ProtectedRoute

Wraps pages that require authentication. Redirects to `/login?redirectTo=` if not authenticated. Renders a loading spinner while auth state resolves.

## ProgressTracker

- Polls `GET /api/v1/pipeline/status/{jobId}` every 3 seconds
- Displays progress bar, current stage label, and phase checklist (all 14 stages)
- Auto-redirects to `/results/[jobId]` on completion
- Stops polling on failure and shows error

## ThreeViewer

- Renders GLB mesh or PLY point cloud via React Three Fiber
- Mesh/Point Cloud toggle buttons
- Orbit controls (rotate, zoom, pan)
- Auto-fit camera to bounding box
- Fullscreen mode
- Handles Float64→Float32 conversion for PLY

## DownloadPanel

- Fetches artifact availability via `GET /api/v1/download/{jobId}`
- Renders categorized download buttons (3D Assets / Image Artifacts / Metadata)
- Triggers direct file download via `<a>` click

## Navbar

- Auth-aware: shows Login/Signup for guests, History/Profile/Logout for authenticated users
- Active route highlighting
- Logo + brand name

## HistoryGrid

- Paginated grid of job cards
- Search by filename, filter by status, sort by newest/oldest
- Delete button with confirmation
- Fetches from `GET /api/v1/history` with query params

---

# State Management

## AuthContext (React Context + Supabase)

- Provides `user`, `session`, `loading`, `logout` globally
- Initializes from `supabase.auth.getSession()`
- Listens to `onAuthStateChange` for sign-in/sign-out events
- All protected pages use `useAuth()` to attach `Authorization: Bearer` headers

## Local State (per page)

- Page-level `useState` for forms, loading, error, previews
- No global store (Redux/Zustand) — kept intentionally minimal

---

# API Communication

All API calls use native `fetch()` — no Axios or service wrappers.

- Upload: `POST /api/v1/upload` (FormData with `Authorization` header)
- Status polling: `GET /api/v1/pipeline/status/{jobId}`
- Results: `GET /api/v1/download/{jobId}/result` (with `?token=` fallback for direct URLs)
- Downloads: `GET /api/v1/download/{jobId}/{artifactKey}?token=...`
- History: `GET /api/v1/history?...` + `DELETE /api/v1/history/{jobId}`
- Profile: `GET /api/v1/profile`

API base URL configured via `NEXT_PUBLIC_API_URL` env var (default `http://localhost:8000/api/v1`).

---

# Pipeline Stages (Frontend Display)

```
  Upload
  Image Validation
  Image Analysis
  CLAHE Enhancement
  Florence-2 Captioning
  GroundingDINO Detection
  Florence-2 Part Detection
  SAM2.1 Segmentation
  Background Removal
  Hunyuan3D-2 Shape Generation
  Hunyuan3D-2 Texture Generation
  Mesh Validation
  Point Cloud Generation
  DBSCAN Segmentation
```

Displayed in ProgressTracker phase list with check/active/pending states.

---

# File Validation

| Rule | Value |
|------|-------|
| Formats | JPG, JPEG, PNG, WEBP, BMP |
| Max Size | 25 MB |
| Checks | Extension, file size, image readability |

---

# Theme

| Token | Color |
|-------|-------|
| Primary | Blue (gradient) |
| Background | Slate-950 |
| Card | Glass (backdrop-blur) |
| Success | Emerald |
| Error | Red |
| Warning | Amber |

---

# Performance

- Lazy loading via Next.js dynamic imports
- Three.js scene loads on demand
- Image optimization with next/image compatible patterns
- Polling stops on completion/failure

---

# Security

- JWT token sent in `Authorization` header for all authenticated requests
- File type/size validated client-side before upload
- Auth routes wrapped in `ProtectedRoute` redirect guard
- Supabase session management via `onAuthStateChange`
