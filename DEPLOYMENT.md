# Deploy Style Savvy for Free (GitHub + Free Tiers)

Deploy the full app (API + web + database + images) for free using your GitHub account. All services below have free tiers that work with GitHub login.

---

## Quick steps (hosting with GitHub)

1. **GitHub** — Push your code to a repo. Sign in at [github.com](https://github.com), create a new repo, then push from your machine (see Step 1 below).
2. **Supabase** — Create a project, get your **Database URI**. You’ll paste it into Render as `DATABASE_URL`.
3. **Cloudinary** — Create an account, get **Cloud name**, **API Key**, **API Secret**. You’ll paste these into Render.
4. **Render** — Sign in with GitHub, create a **Web Service** from your repo. Set env vars (DATABASE_URL, Cloudinary, DEBUG=false). Copy the service URL (e.g. `https://style-savvy-api.onrender.com`).
5. **Vercel or Netlify** — Sign in with GitHub, import your repo. Set **root directory** to `web`, add env var **VITE_API_BASE_URL** = your Render URL. Deploy.
6. Open your Vercel/Netlify URL — the app is live.

Details for each step are in the sections below.

---

## Overview

| Part        | Service    | Free tier        | Role                          |
|------------|------------|------------------|-------------------------------|
| **Code**   | GitHub     | Free             | Host repo, trigger deploys    |
| **API**    | Render     | Free web service | Run FastAPI backend           |
| **Web**    | Vercel or Netlify | Free        | Serve React app (static)      |
| **Database** | Supabase | Free PostgreSQL  | Store users + clothing        |
| **Images** | Cloudinary | Free             | Store uploaded photos         |

---

## Step 1: Push your code to GitHub

If the repo is not on GitHub yet:

```bash
cd /path/to/whattowear
git init
git add .
git commit -m "Initial commit – Style Savvy"
# Create a new repo on GitHub (github.com/new), then:
git remote add origin https://github.com/YOUR_USERNAME/whattowear.git
git branch -M main
git push -u origin main
```

Keep `.env` and `web/.env` out of the repo (they are in `.gitignore`). You’ll set the same values as environment variables in each hosting service.

---

## Step 2: Database (Supabase) – free

1. Go to [supabase.com](https://supabase.com) → **Start your project** → sign in with GitHub.
2. **New project** → pick org, name (e.g. `style-savvy`), database password, region → **Create**.
3. In the project: **Settings** → **Database**.
4. Under **Connection string** choose **URI** and copy it. It looks like:
   ```text
   postgresql://postgres.[ref]:[YOUR-PASSWORD]@aws-0-[region].pooler.supabase.com:6543/postgres
   ```
5. Replace `[YOUR-PASSWORD]` with your database password. Save this as `DATABASE_URL` for the API (Step 4).

Tables (`users`, `clothing_items`) are created automatically when the API runs.

---

## Step 3: Images (Cloudinary) – free

1. Go to [cloudinary.com](https://cloudinary.com) → sign up (free).
2. In **Dashboard** note:
   - **Cloud name**
   - **API Key**
   - **API Secret** (click “Reveal”)
3. Save these for the API (Step 4):  
   `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`.

---

## Step 4: API (Render) – free

1. Go to [render.com](https://render.com) → **Get started** → sign in with **GitHub**.
2. **New** → **Web Service**.
3. Connect the **whattowear** repo (or the one you pushed).
4. Configure:
   - **Name:** `style-savvy-api` (or any name).
   - **Region:** choose one close to you.
   - **Branch:** `main`.
   - **Runtime:** **Python 3**.
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
   - **Root directory:** leave blank (repo root).
5. **Environment** (Add Environment Variable):
   - `DATABASE_URL` = your Supabase URI from Step 2.
   - `CLOUDINARY_CLOUD_NAME` = from Step 3.
   - `CLOUDINARY_API_KEY` = from Step 3.
   - `CLOUDINARY_API_SECRET` = from Step 3.
   - `DEBUG` = `false`
6. **Create Web Service**. Wait for the first deploy.
7. Copy the service URL, e.g. `https://style-savvy-api.onrender.com` — this is your **API base URL** for the frontend.

Note: On the free tier the service may spin down after ~15 minutes of no traffic; the first request after that can be slow (cold start).

---

## Step 5: Web app (Vercel) – free

1. Go to [vercel.com](https://vercel.com) → **Sign up** → use **GitHub**.
2. **Add New** → **Project** → import the **whattowear** repo.
3. Configure:
   - **Root directory:** click **Edit** → set to `web`.
   - **Framework preset:** Vite (should be auto-detected).
   - **Build command:** `npm run build`
   - **Output directory:** `dist`
4. **Environment variables** (add for Production, and Preview if you want):
   - `VITE_API_BASE_URL` = your Render API URL from Step 4, e.g. `https://style-savvy-api.onrender.com`  
   (no trailing slash)
5. **Deploy**. When it’s done, Vercel gives you a URL like `https://whattowear-xxx.vercel.app`.

Open that URL: the app will call your Render API and use Supabase + Cloudinary.

---

## Alternative: Web app on Netlify

1. Go to [netlify.com](https://netlify.com) → **Sign up** → **Log in with GitHub**.
2. **Add new site** → **Import an existing project** → choose GitHub and the **whattowear** repo.
3. Settings:
   - **Base directory:** `web`
   - **Build command:** `npm run build`
   - **Publish directory:** `dist`
4. **Environment variables** → **Add**:
   - `VITE_API_BASE_URL` = your Render API URL (e.g. `https://style-savvy-api.onrender.com`)
5. **Deploy site**.

---

## Checklist

- [ ] Code pushed to GitHub (no `.env` in repo).
- [ ] Supabase project created; `DATABASE_URL` copied.
- [ ] Cloudinary account created; cloud name, API key, API secret copied.
- [ ] Render web service created; env vars set; API URL copied.
- [ ] Vercel (or Netlify) project created with root `web`, `VITE_API_BASE_URL` set to Render URL.
- [ ] Visit the Vercel/Netlify URL and test: Profile photo, Wardrobe upload, Recommendations.

---

## Optional: Render Blueprint

The repo includes `render.yaml`. In Render you can use **Blueprints** → **New Blueprint** → connect the repo. Render will create the web service from the file; you still need to add the environment variables in the Render dashboard.

---

## Troubleshooting

- **API 503 or “service unavailable”**  
  Free tier may be spinning up. Wait 30–60 seconds and try again.

- **CORS errors in browser**  
  The API allows all origins (`allow_origins=["*"]`). If you use a custom domain for the frontend, you can restrict CORS in `api/main.py` to that domain.

- **Images not loading**  
  Confirm Cloudinary env vars are set on Render and that uploads succeed (check Render logs).

- **Database errors**  
  Check Supabase connection string (password, port 6543 for pooler). Ensure the API has run at least once so tables are created.

- **Frontend shows “Request failed”**  
  Ensure `VITE_API_BASE_URL` on Vercel/Netlify is exactly your Render URL (https, no trailing slash). Redeploy after changing env vars.

---

**Style Savvy** — deployed for free with GitHub + Render + Vercel/Netlify + Supabase + Cloudinary.
