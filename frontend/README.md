# 3D Model Processing Pipeline — Frontend

Next.js 15 frontend for the Automated Single-Image to 3D Asset and Point Cloud Generation System. Users upload an image, and the backend generates a textured 3D model (GLB) and segmented point cloud (PLY).

## Pages

| Route | Description |
|---|---|
| `/` | Landing page |
| `/upload` | Image upload with drag-and-drop |
| `/processing/[jobId]` | Real-time pipeline progress tracker |
| `/results/[jobId]` | 3D model viewer, point cloud viewer, download panel |
| `/viewer` | Standalone 3D viewer (redirect) |
| `/download` | Download center (redirect) |
| `/login` | Supabase authentication |
| `/signup` | User registration |
| `/forgot-password` | Password reset |
| `/profile` | User profile / dashboard |
| `/history` | Past project history |

## Environment Variables

| Variable | Description |
|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anonymous key |
| `NEXT_PUBLIC_BACKEND_URL` | Backend base URL (e.g. `http://localhost:8000`) |
| `NEXT_PUBLIC_API_URL` | Backend API URL (e.g. `http://localhost:8000/api/v1`) |

## Getting Started

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Build

```bash
npm run build
```
