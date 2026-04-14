# JARVIS Backend — 100% Free Setup

Uses **Groq API** (free, no credit card) + **Railway** or **Vercel** (free hosting).

---

## FOLDER STRUCTURE

You need 2 separate GitHub repos:

### Repo 1 — jarvis-backend (this folder)
```
jarvis-backend/
├── main.py
├── requirements.txt
├── railway.json
├── vercel.json
├── .env.example
└── README.md
```

### Repo 2 — jarvis-frontend
```
jarvis-frontend/
└── index.html        ← the HTML file you have
```

---

## STEP 1 — Get Free Groq API Key

1. Go to https://console.groq.com
2. Sign up (free, no credit card)
3. Go to API Keys → Create API Key
4. Copy the key — looks like: gsk_xxxxxxxxxxxx

---

## STEP 2 — Deploy Backend (Pick ONE option below)

### Option A: Railway (recommended, easiest)

1. Go to https://railway.app and sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your `jarvis-backend` repo
4. Click "Add Variables" and add:
   - GROQ_API_KEY = gsk_your_key_here
   - ALLOWED_ORIGINS = *
5. Railway auto-deploys. You get a URL like:
   https://jarvis-backend-production.up.railway.app

### Option B: Vercel (same place as frontend)

1. Go to https://vercel.com
2. New Project → import `jarvis-backend` repo
3. Framework Preset = "Other"
4. Go to Settings → Environment Variables → add:
   - GROQ_API_KEY = gsk_your_key_here
   - ALLOWED_ORIGINS = *
5. Deploy. URL will be like:
   https://jarvis-backend.vercel.app

---

## STEP 3 — Update Frontend with Backend URL

Open index.html, find this line near the bottom:

    const JARVIS_API = "https://your-jarvis-backend.onrender.com";

Change it to your actual backend URL from Step 2, e.g.:

    const JARVIS_API = "https://jarvis-backend-production.up.railway.app";

---

## STEP 4 — Deploy Frontend on Vercel

1. Push index.html to your `jarvis-frontend` GitHub repo
2. Vercel → New Project → import `jarvis-frontend`
3. Framework = "Other" → Deploy
4. Done! Your site is live at: https://jarvis-frontend.vercel.app

---

## STEP 5 — Lock down CORS (optional but recommended)

Once you have your Vercel frontend URL, go back to Railway/Vercel backend
and update the environment variable:

    ALLOWED_ORIGINS = https://jarvis-frontend.vercel.app

---

## SUMMARY

| What          | Where    | Cost |
|---------------|----------|------|
| index.html    | Vercel   | FREE |
| main.py etc   | Railway  | FREE |
| AI (Llama 3)  | Groq API | FREE |

Total cost = $0
