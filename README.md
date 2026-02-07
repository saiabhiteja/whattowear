# Style Savvy

**AI-powered outfit suggestions based on your skin tone, weather, and occasion.**

Style Savvy is a full-stack personal wardrobe app. Upload a photo of yourself for skin analysis, add your clothes with photos, then get tailored outfit recommendations for any event, weather, and time of day—no login required (single-user MVP).

---

## Features

- **Skin analysis** — Upload a face photo; the app detects skin tone (Fair / Medium / Dark) and undertone (Warm / Cool / Neutral) using OpenCV and LAB color space.
- **Wardrobe management** — Add clothing with a photo; dominant colors are extracted automatically via KMeans clustering.
- **Smart recommendations** — Get top 3 outfit suggestions with scores and reasons (event match, weather, skin compatibility, time of day).
- **Modern UI** — React + TypeScript web app with Tailwind and shadcn/ui; FastAPI API with Swagger docs.

---

## Tech Stack

| Layer      | Technology |
|-----------|------------|
| **Web**      | React 18, TypeScript, Vite, Tailwind CSS, shadcn/ui, React Router |
| **API**      | FastAPI (Python 3.11+) |
| **Image**    | OpenCV, NumPy, scikit-learn (KMeans), Cloudinary |
| **Database** | PostgreSQL (Supabase) or SQLite (local) |
| **Auth**     | None (single-user MVP) |

---

## Project Structure

```
style-savvy/                    # or your repo name
├── api/                        # Backend API (FastAPI)
│   ├── main.py                 # App entry, CORS, routes
│   ├── config.py               # Settings from .env
│   ├── database.py             # SQLAlchemy engine, session
│   ├── constants/              # Enums, color palettes, score weights
│   ├── exceptions/             # Custom domain exceptions
│   ├── models/                 # SQLAlchemy models (User, Clothing)
│   ├── schemas/                # Pydantic request/response schemas
│   ├── services/               # Image, color, skin tone, recommendation
│   └── routes/                 # User, clothing, recommendation endpoints
├── web/                        # Web app (React + Vite)
│   ├── src/
│   │   ├── lib/api.ts          # API client and types
│   │   ├── pages/              # Dashboard, Profile, Wardrobe, Recommendations
│   │   └── components/        # UI components
│   ├── package.json
│   ├── vite.config.ts
│   └── .env.example            # VITE_API_BASE_URL
├── .env.example                # API env template
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## Prerequisites

- **Node.js** 18+ and **npm** (for web app)
- **Python** 3.11+ (for API)
- **PostgreSQL** (Supabase free tier) or use **SQLite** for local-only runs
- **Cloudinary** account (free tier) for image storage

---

## Quick Start

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <repo-folder>
```

### 2. API setup

```bash
# Create and activate a virtual environment (name it venv for a clean, standard setup)
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template and fill in your values
cp .env.example .env
```

Edit `.env` with your database URL and Cloudinary credentials (see [Environment variables](#environment-variables)).

> **Note:** If you already have a virtual environment folder named `wardrobe-env`, rename it to `venv` for consistency: `mv wardrobe-env venv`.

### 3. Web app setup

```bash
cd web
npm install
cp .env.example .env
```

Edit `web/.env` and set the API base URL (default for local: `http://localhost:8000`).

### 4. Run the app

**Terminal 1 — API**

```bash
# From project root
source venv/bin/activate
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 — Web app**

```bash
cd web
npm run dev
```

- **Web app:** http://localhost:5173  
- **API docs:** http://localhost:8000/docs  

---

## Environment Variables

### Backend (project root `.env`)

| Variable | Description | Example |
|---------|-------------|---------|
| `DATABASE_URL` | PostgreSQL or SQLite connection string | `postgresql://user:pass@host:5432/db` or `sqlite:///./app.db` |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name | From Cloudinary dashboard |
| `CLOUDINARY_API_KEY` | Cloudinary API key | From Cloudinary dashboard |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | From Cloudinary dashboard |
| `DEBUG` | Enable debug mode | `true` or `false` |

### Web app (`web/.env`)

| Variable | Description | Example |
|---------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API base URL | `http://localhost:8000` (dev) or your deployed API URL |

---

## Database Setup (Supabase)

1. Create a free account at [supabase.com](https://supabase.com) and create a new project.
2. In **Settings → Database**, copy the **Connection string** (URI). Use the **Transaction** pooler (port **6543**) if shown.
3. Replace the placeholder password in the URI with your database password.
4. Set `DATABASE_URL` in your backend `.env` to this URI.

Tables (`users`, `clothing_items`) are created automatically when the API starts.

**Local development without Supabase:** set `DATABASE_URL=sqlite:///./wardrobe_local.db` in `.env`. No PostgreSQL needed.

---

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/` | Health check |
| `POST` | `/user/upload-photo` | Upload face photo → skin tone & undertone |
| `GET`  | `/user/profile` | Get user profile (skin analysis) |
| `POST` | `/clothing/upload` | Upload clothing image + metadata (type, occasion, season) |
| `GET`  | `/clothing/all` | List all clothing items |
| `POST` | `/recommendation/suggest` | Get top 3 outfit suggestions (body: `event`, `weather`, `time_of_day`) |

Interactive API documentation: **http://localhost:8000/docs** when the API is running.

---

## How It Works

- **Skin analysis:** Face is detected with OpenCV’s Haar Cascade; skin region is converted to LAB color space. Lightness (L) gives skin tone; the b channel gives undertone.
- **Clothing colors:** Each clothing image is resized and clustered with KMeans; dominant (and optional secondary) colors are mapped to labels (e.g. BLACK, BLUE, RED).
- **Recommendations:** A rule-based engine scores each clothing item (event match, weather/season, skin tone/undertone, time of day) and returns the top 3 with explanations.

---

## Deployment

**Free deployment (GitHub + Render + Vercel + Supabase + Cloudinary):** see **[DEPLOYMENT.md](./DEPLOYMENT.md)** for step-by-step instructions.

- **API:** [Render](https://render.com) — Build: `pip install -r requirements.txt`. Start: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`. Optional: use `render.yaml` blueprint.
- **Web app:** [Vercel](https://vercel.com) or [Netlify](https://netlify.com) — Root: `web`, build: `npm run build`, set `VITE_API_BASE_URL` to your API URL.
- **Database:** [Supabase](https://supabase.com) — Set `DATABASE_URL` in the API environment.
- **Images:** [Cloudinary](https://cloudinary.com) — Set Cloudinary env vars in the API environment (required for production; local dev can use `./uploads/`).

---

## License

MIT (or your chosen license).

---

**Style Savvy** — *Look good, feel confident.*
