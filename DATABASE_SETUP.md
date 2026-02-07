# Database Setup Guide — Supabase PostgreSQL

Step-by-step instructions to create your free PostgreSQL database on Supabase.

---

## Step 1: Create a Supabase Account

1. Go to **https://supabase.com**
2. Click **"Start your project"**
3. Sign up with **GitHub** (recommended) or email
4. You're on the free tier by default (no credit card needed)

---

## Step 2: Create a New Project

1. Click **"New Project"**
2. Fill in:
   - **Name**: `wardrobe-ai`
   - **Database Password**: Choose a strong password — **save this, you'll need it**
   - **Region**: Pick the closest to you (e.g., `South Asia (Mumbai)` for India)
3. Click **"Create new project"**
4. Wait 1-2 minutes for provisioning

---

## Step 3: Get Your Connection String

1. In your project dashboard, go to **Settings** (gear icon in sidebar)
2. Click **"Database"** under Configuration
3. Scroll to **"Connection string"** section
4. Select **"URI"** tab
5. Copy the connection string. It looks like:

```
postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
```

6. **Replace `[password]`** with the database password you set in Step 2

> **Important**: Use the **"Transaction" pooler (port 6543)** connection for best compatibility with SQLAlchemy.

---

## Step 4: Update Your `.env` File

Open `/whattowear/.env` and update the `DATABASE_URL`:

```env
DATABASE_URL=postgresql://postgres.[your-project-ref]:[your-password]@aws-0-[region].pooler.supabase.com:6543/postgres

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

---

## Step 5: Set Up Cloudinary (for Image Storage)

1. Go to **https://cloudinary.com**
2. Sign up for a **free account**
3. From your **Dashboard**, copy:
   - **Cloud Name**
   - **API Key**
   - **API Secret**
4. Paste them into your `.env` file

---

## Step 6: Run the App

The database tables are created **automatically** when the app starts (SQLAlchemy `create_all`).

```bash
cd "/Users/saiabhitejac/Abhi Projects/whattowear"
source wardrobe-env/bin/activate
uvicorn app.main:app --reload
```

You should see in the logs:
```
Database tables initialized successfully
Application started successfully
```

---

## Step 7: Verify Tables in Supabase

1. Go to your Supabase project dashboard
2. Click **"Table Editor"** in the sidebar
3. You should see two tables:
   - **users** — columns: `id`, `photo_url`, `skin_tone`, `skin_undertone`, `created_at`, `updated_at`
   - **clothing_items** — columns: `id`, `image_url`, `dominant_color`, `secondary_color`, `clothing_type`, `occasion`, `season`, `created_at`

---

## Step 8: Test the Full Flow

Open **http://localhost:8000/docs** (Swagger UI) and test:

1. **POST /user/upload-photo** — Upload a clear face photo (JPEG/PNG)
   - Check Supabase Table Editor → `users` table to see skin_tone and skin_undertone

2. **POST /clothing/upload** — Upload a clothing image + select type/occasion/season
   - Check `clothing_items` table to see the detected colors

3. **POST /recommendation/suggest** — Send event/weather/time_of_day
   - Get back scored outfit suggestions

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Connection refused` | Check DATABASE_URL is correct, password has no special chars unescaped |
| `relation does not exist` | Restart the app — tables are created on startup |
| `Cloudinary upload failed` | Verify your cloud_name, api_key, api_secret in `.env` |
| `No face detected` | Upload a clear, front-facing photo with good lighting |
| `psycopg2 error` | Make sure you're using the `wardrobe-env` virtual environment |

---

## Free Tier Limits (you won't hit these for MVP)

| Service | Free Tier |
|---------|-----------|
| **Supabase** | 500MB database, unlimited API requests, 2 projects |
| **Cloudinary** | 25GB storage, 25GB bandwidth/month |
| **Render** (for deploy) | 750 hours/month, auto-sleep after 15 min inactivity |
