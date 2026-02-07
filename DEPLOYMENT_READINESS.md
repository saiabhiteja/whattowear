# Deployment Readiness – Style Savvy

**Verdict: Ready for deployment** with the checklist below.

---

## Summary

| Area | Status | Notes |
|------|--------|--------|
| **API (Render)** | Ready | Env from dashboard; uploads dir created before mount; Cloudinary required in prod |
| **Web (Vercel)** | Ready | Set root `web`, `VITE_API_BASE_URL`; build uses `vite build` |
| **Secrets** | OK | No hardcoded secrets; .env in .gitignore |
| **Database** | OK | Supabase URI set as `DATABASE_URL` on Render |
| **CORS** | OK | Allow-all for MVP; can restrict to frontend URL later |

---

## API (Render) – Checklist

- [x] **Start command** uses `$PORT`: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
- [x] **Build command**: `pip install -r requirements.txt`
- [x] **Uploads directory** created before `StaticFiles` mount (avoids RuntimeError on Render)
- [x] **Config** reads from environment; `.env` optional (missing file ignored by pydantic-settings)
- [x] **Health check**: `GET /` returns `{"status":"healthy"}`
- [ ] **Environment variables** set in Render Dashboard:
  - `DATABASE_URL` (Supabase URI)
  - `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`
  - `DEBUG=false`

---

## Web (Vercel) – Checklist

- [x] **Root directory**: `web`
- [x] **Build command**: `npm run build` (default)
- [x] **Output**: `dist` (Vite default)
- [x] **API URL** from env: `VITE_API_BASE_URL` (no hardcoded production URL)
- [ ] **Environment variable** set in Vercel: `VITE_API_BASE_URL` = your Render API URL (e.g. `https://style-savvy-api.onrender.com`)

---

## Optional Improvements (not required for launch)

1. **CORS** – Restrict `allow_origins` to your Vercel/Netlify URL in production for tighter security.
2. **Log level** – Use `DEBUG` to set logging level (e.g. INFO vs DEBUG).
3. **Request size** – Add explicit upload size limits in FastAPI if you want to cap image size.

---

## Quick pre-deploy check

**Local:**

```bash
# API
cd /path/to/whattowear && source venv/bin/activate
uvicorn api.main:app --host 0.0.0.0 --port 8000

# Web (other terminal)
cd web && npm run build && npm run preview
```

**After deploy:**

- Open Vercel URL → app loads.
- Profile → upload photo → no CORS/network errors.
- Wardrobe → add clothing → no errors.
- Recommendations → returns suggestions.

---

*Last checked: config, main.py, vite.config.ts, api.ts, requirements.txt, render.yaml, .gitignore.*
