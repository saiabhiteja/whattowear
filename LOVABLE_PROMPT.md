# Lovable Frontend Prompt

Copy-paste the prompt below into Lovable to generate your frontend.

---

## PROMPT START

Build a modern, beautiful single-page web app called **"WhatToWear"** — an AI-powered wardrobe recommendation system.

### TECH STACK
- React + TypeScript
- Tailwind CSS for styling
- shadcn/ui components
- React Router for navigation
- Axios or fetch for API calls

### BACKEND API (already built, do NOT create a backend)
The backend is a FastAPI server. Configure the base URL as an environment variable:
```
VITE_API_BASE_URL=http://localhost:8000
```

### API ENDPOINTS TO CONNECT TO

1. **POST /user/upload-photo** — Upload face photo (multipart form, field name: `photo`)
   - Response: `{ message, photo_url, skin_tone, skin_undertone }`

2. **GET /user/profile** — Get user profile
   - Response: `{ id, photo_url, skin_tone, skin_undertone, created_at, updated_at }`

3. **POST /clothing/upload** — Upload clothing image (multipart form)
   - Fields: `image` (file), `clothing_type`, `occasion`, `season` (all as form data)
   - clothing_type options: SHIRT, TSHIRT, JEANS, TROUSERS, KURTA, JACKET, SHORTS, DRESS, BLAZER, HOODIE
   - occasion options: CASUAL, OFFICE, PARTY, WEDDING, TRADITIONAL
   - season options: SUMMER, WINTER, ALL
   - Response: `{ id, image_url, dominant_color, secondary_color, clothing_type, occasion, season, created_at }`

4. **GET /clothing/all** — Get all clothing items
   - Response: array of clothing objects

5. **POST /recommendation/suggest** — Get outfit suggestions
   - Body (JSON): `{ event: "OFFICE"|"CASUAL"|"PARTY"|"WEDDING", weather: "HOT"|"COLD"|"RAINY", time_of_day: "DAY"|"NIGHT" }`
   - Response: `{ suggestions: [{ clothing: {...}, score: number, reasons: string[] }], event, weather, time_of_day }`

6. **GET /** — Health check
   - Response: `{ status: "healthy", app: "..." }`

### PAGES & LAYOUT

**Navigation**: Sidebar or top navbar with 4 sections:
1. **Dashboard** (home)
2. **My Profile** (skin analysis)
3. **My Wardrobe** (clothing gallery)
4. **Get Recommendations** (outfit suggestions)

### PAGE DETAILS

#### 1. Dashboard (`/`)
- Welcome hero section with app name "WhatToWear" and tagline: "AI-powered outfit suggestions based on your skin tone, weather, and occasion"
- Quick stats cards showing: number of clothing items, skin analysis status (done/pending), last recommendation
- Quick action buttons: "Upload Photo", "Add Clothing", "Get Suggestions"
- Clean, modern design with gradient backgrounds

#### 2. My Profile (`/profile`)
- If no photo uploaded: show a large upload area with drag-and-drop or click-to-upload for face photo
- Upload button triggers POST /user/upload-photo
- After upload, show:
  - User's photo (from photo_url)
  - Skin tone badge (FAIR / MEDIUM / DARK) with appropriate color indicator
  - Skin undertone badge (WARM / COOL / NEUTRAL)
  - "Re-analyze" button to upload a new photo
- Use a clean card layout

#### 3. My Wardrobe (`/wardrobe`)
- "Add Clothing" button opens a modal/drawer with:
  - Image upload area (drag and drop)
  - Dropdown for Clothing Type (SHIRT, TSHIRT, JEANS, etc.)
  - Dropdown for Occasion (CASUAL, OFFICE, PARTY, etc.)
  - Dropdown for Season (SUMMER, WINTER, ALL)
  - Submit button
- Clothing grid: show all items as cards with:
  - Clothing image
  - Dominant color shown as a colored circle/badge
  - Clothing type, occasion, season as small tags
- Empty state: friendly illustration/message saying "Your wardrobe is empty. Start by adding some clothes!"
- Filter/sort options by type, occasion, or season

#### 4. Get Recommendations (`/recommendations`)
- Form section with 3 dropdowns:
  - Event: OFFICE, CASUAL, PARTY, WEDDING
  - Weather: HOT, COLD, RAINY
  - Time of Day: DAY, NIGHT
- Big "Get Suggestions" button
- Results section showing top 3 recommended items as cards:
  - Clothing image
  - Score displayed as a visual meter or badge (e.g., "Score: 8/12")
  - Reasons listed as green check-mark bullet points explaining why this was recommended
  - Clothing metadata (type, occasion, color)
- If no results, show a friendly message

### DESIGN GUIDELINES
- Color scheme: Use a modern palette — deep indigo/purple primary, soft white/gray backgrounds, accent colors for scores
- Typography: Clean sans-serif, good hierarchy
- Spacing: Generous padding, breathable layout
- Animations: Subtle hover effects on cards, smooth page transitions
- Mobile responsive: Must work well on phone screens
- Loading states: Show skeleton loaders or spinners during API calls
- Toast notifications: Show success/error toasts for uploads and actions
- Dark mode support would be a nice bonus

### IMPORTANT
- This is a single-user app, no login/auth needed
- All API calls go to the FastAPI backend (configurable base URL)
- Handle API errors gracefully with user-friendly error messages
- Show loading indicators during image uploads (they take a few seconds)
- The app should feel polished and professional — this is a portfolio project

## PROMPT END
