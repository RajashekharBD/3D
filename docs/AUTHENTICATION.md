# Authentication & History Management System Setup

This document describes the design, schema, flow, and setup guide for the Supabase-integrated User Authentication and Job History Management system.

---

## 1. Authentication Flow

```
User (Browser)
    │
    ├─► Sign Up / Login (Email/Password) ──► Supabase Auth
    │                                             │
    │                                        (Generates JWT)
    │                                             │
    ├─► Request with Bearer Token ◄───────────────┘
    │
    ▼
FastAPI Backend
    │
    ├─► Validate JWT Token (jose HS256 locally using SUPABASE_JWT_SECRET)
    │
    ├─► Extract User ID & Email
    │
    └─► Run Pipeline / Query Database (Filter all queries by User ID)
```

---

## 2. Database Schema

The system uses three tables in PostgreSQL, guarded by Row Level Security (RLS) policies:

### `profiles` Table
- `id`: `UUID` (Primary Key, references `auth.users.id` cascade)
- `email`: `TEXT` (Unique, not null)
- `created_at`: `TIMESTAMP WITH TIME ZONE`
- `updated_at`: `TIMESTAMP WITH TIME ZONE`
- `last_login`: `TIMESTAMP WITH TIME ZONE`

### `jobs` Table
- `job_id`: `UUID` (Primary Key)
- `user_id`: `UUID` (References `profiles.id` cascade)
- `original_filename`: `TEXT` (not null)
- `status`: `TEXT` (uploaded / processing / completed / failed)
- `started_at`: `TIMESTAMP WITH TIME ZONE`
- `completed_at`: `TIMESTAMP WITH TIME ZONE`
- `processing_duration_seconds`: `DOUBLE PRECISION`
- `model_generated`: `BOOLEAN`
- `pointcloud_generated`: `BOOLEAN`
- `error_message`: `TEXT`
- `is_deleted`: `BOOLEAN` (Soft delete flag)

### `artifacts` Table
- `id`: `UUID` (Primary Key)
- `job_id`: `UUID` (References `jobs.job_id` cascade)
- `artifact_type`: `TEXT` (e.g. `'model'`, `'rgba'`, `'pointcloud'`)
- `file_path`: `TEXT`
- `file_size`: `BIGINT`
- `mime_type`: `TEXT`

---

## 3. Environment Variables

### Backend Configuration (`.env`)
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_JWT_SECRET=your-jwt-secret-from-api-settings
```

### Frontend Configuration (`frontend/.env.local`)
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-public-key
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

---

## 4. Local Development

1. **Supabase Project**: Setup a free database project at [supabase.com](https://supabase.com).
2. **Apply Migration**: Copy the contents of `supabase/migrations/20260717000000_auth_history_schema.sql` into the Supabase **SQL Editor** and run it to create tables, indexes, RLS policies, and triggers.
3. **Configure Auth**: Enable Email/Password signup in the Supabase Auth providers dashboard.
4. **Run Backend**: Add env variables and launch the FastAPI server.
5. **Run Frontend**: Add public client env variables and run `npm run dev`.
