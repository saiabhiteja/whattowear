# AI Wardrobe Recommendation System

A personal AI wardrobe recommendation system that analyzes skin tone and clothing colors to suggest outfits based on event, weather, and time of day.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   FastAPI Server                     │
│                                                     │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │  User     │  │  Clothing    │  │ Recommendation│ │
│  │  Routes   │  │  Routes      │  │ Routes        │ │
│  └────┬─────┘  └──────┬───────┘  └───────┬───────┘ │
│       │               │                  │          │
│  ┌────▼─────┐  ┌──────▼───────┐  ┌───────▼───────┐ │
│  │ Skin     │  │  Color       │  │ Recommendation│ │
│  │ Tone     │  │  Service     │  │ Service       │ │
│  │ Service  │  │              │  │ (Rule-based)  │ │
│  └────┬─────┘  └──────┬───────┘  └───────────────┘ │
│       │               │                             │
│  ┌────▼───────────────▼──────┐                     │
│  │     Image Service          │                     │
│  │  (Cloudinary + OpenCV)     │                     │
│  └────────────────────────────┘                     │
│                                                     │
│  ┌────────────────────────────┐                     │
│  │     PostgreSQL (Supabase)  │                     │
│  └────────────────────────────┘                     │
└─────────────────────────────────────────────────────┘
```

## How Color Analysis Works

### Skin Tone Analysis
1. **Face Detection**: OpenCV Haar Cascade detects the face in the uploaded photo
2. **Skin Region Extraction**: The forehead-to-cheek area is cropped (avoids eyes, mouth, hair)
3. **LAB Conversion**: Skin pixels are converted to LAB color space
4. **Classification**:
   - **L channel** (lightness) determines skin tone: FAIR / MEDIUM / DARK
   - **b channel** (yellow-blue axis) determines undertone: WARM / COOL / NEUTRAL

### Clothing Color Extraction
1. **Resize**: Image is resized to 300x300 for fast processing
2. **KMeans Clustering**: Pixels are grouped into 3 clusters
3. **Dominant Color**: The largest cluster's center becomes the primary color
4. **Color Labeling**: RGB values are mapped to the nearest human-readable label (BLACK, BLUE, RED, etc.) using Euclidean distance

## How Recommendation Logic Works

The engine uses **rule-based scoring** (no ML):

| Rule | Points | Example |
|------|--------|---------|
| Event matches occasion | +3 | OFFICE event + OFFICE clothing |
| Weather-appropriate color | +2 | HOT weather + WHITE clothing |
| Season matches weather | +2 | SUMMER clothing + HOT weather |
| Skin tone complement | +2 | DARK skin + bright colors |
| Undertone harmony | +2 | WARM undertone + earth tones |
| Time-of-day color | +1 | NIGHT + BLACK clothing |

Top 3 items by score are returned with explanations.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/user/upload-photo` | Upload face photo for skin analysis |
| GET | `/user/profile` | Get user profile with skin data |
| POST | `/clothing/upload` | Upload clothing image with metadata |
| GET | `/clothing/all` | List all wardrobe items |
| POST | `/recommendation/suggest` | Get outfit suggestions |
| GET | `/` | Health check |

## Setup & Run

### 1. Prerequisites
- Python 3.11+
- PostgreSQL database (Supabase free tier)
- Cloudinary account (free tier)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file (see `.env.example`):
```
DATABASE_URL=postgresql://user:pass@host:5432/dbname
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### 4. Run the Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Open API Docs
Visit `http://localhost:8000/docs` for interactive Swagger UI.

## Free-Tier Deployment

### Render (Backend)
- Create a new **Web Service** on [Render](https://render.com)
- Connect your GitHub repo
- Set build command: `pip install -r requirements.txt`
- Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Add environment variables from `.env`
- Free tier provides 750 hours/month

### Supabase (Database)
- Create a project on [Supabase](https://supabase.com)
- Copy the PostgreSQL connection string
- Set it as `DATABASE_URL` in your environment
- Free tier: 500MB storage, unlimited API requests

### Cloudinary (Images)
- Create account at [Cloudinary](https://cloudinary.com)
- Copy cloud name, API key, and API secret
- Free tier: 25GB storage, 25GB bandwidth/month

## Tech Stack
- **Backend**: FastAPI (Python)
- **Image Processing**: OpenCV, NumPy, scikit-learn
- **Database**: PostgreSQL (Supabase)
- **Image Storage**: Cloudinary
- **Recommendation**: Rule-based scoring (no deep learning)
