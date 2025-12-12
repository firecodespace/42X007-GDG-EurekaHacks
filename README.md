# 🧠 CompeteSync — AI-Powered Competition Discovery & Team Matching Platform
### Built by Team 42X007

---

## 🚀 Overview
CompeteSync is an AI-driven platform designed to help students discover relevant competitions and instantly form high-performance teams. It analyzes events using Google Gemini, computes personalized fit scores, and recommends ideal teammates based on skills, experience, and interests.

Built for university ecosystems, CompeteSync automates the entire journey:
discover → understand → match → participate.

---

## 🎯 Problem Statement
Students face real challenges:
- Difficult to find competitions aligned with their skills  
- Hard to form balanced and complementary teams  
- Event details are scattered across multiple platforms  
- No AI system exists to simplify decision-making for participation  

CompeteSync solves all of this through AI automation, Google Cloud infrastructure, and real-time recommendation pipelines.

---

## ✨ Key Features

### 1. Competition Aggregation
Automatically scrapes competitions from:
- GDG / Google Events  
- Devpost  
- MLH  
- Hack2Skill  
- Unstop  
- University innovation portals  

All events are normalized and stored in Firestore.

---

### 2. Gemini-Powered Event Understanding
Google Gemini processes each competition to extract:
- Required skills  
- Difficulty rating  
- Estimated team size  
- Time commitment  
- AI-generated event summary  
- Category classification (AI/Web/Cloud/Startup/etc.)

---

### 3. Personalized Fit Score
The platform computes a score (0–100%) based on:
- User’s skills  
- Interests  
- Past experience  
- Project history  
- Learning goals  

Competitions are ranked for each user using a custom scoring model.

---

### 4. AI Team Matching Engine
Suggests an optimized team by analyzing:
- Complementary skills  
- Collaboration styles  
- Strength–weakness balance  
- Needed roles (frontend/backend/cloud/ML/design)  

Gemini also generates:
- Team composition reasoning  
- Suggested role distribution  

---

### 5. Modern Dashboard UI
Built using Next.js + Tailwind:
- Competition feed  
- Team suggestions  
- Profile panel  
- Filters & sorting  
- Onboarding modal  
- Real-time updates  

Designed for clarity and speed.

---

# 🛠️ Tech Stack Overview

## Frontend
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Zustand / React Context
- Dynamic & SSR components

---

## Backend
- FastAPI (Python)
- Gemini API integration
- Scraper engine (BeautifulSoup/Playwright)
- Firestore Admin SDK
- Custom AI matching algorithms

---

## Google Cloud Usage
### Cloud Run
- Main backend deployment  
- Auto-scaling microservice  

### Cloud Scheduler
- Runs competition scrapers (cron)

### Cloud Logging
- Backend logs + monitoring

---

## Firebase Usage
- Firebase Auth → user login  
- Cloud Firestore → competitions, profiles, match data  
- Admin SDK → backend write operations  

---

# 🏛️ System Architecture

Frontend (Next.js)
    │
    ▼
Backend API (FastAPI + Gemini)
    │
    ▼
Firestore Database
    │
    ▲
Scraper Engine (Cron Jobs)

---

# 📁 Project Structure

frontend/
  ├── src/
  │   ├── app/                # pages, routes
  │   ├── components/         # UI + dashboard components
  │   ├── lib/                # firebase, api, utils
  │   ├── services/           # frontend APIs
  │   ├── store/              # global state
  │   ├── types/              # TS types
  │   └── hooks/              # custom hooks

backend/
  ├── app/
  │   ├── api/                # FastAPI routes
  │   ├── services/           # Gemini, Firestore, scoring, matching
  │   ├── scrapers/           # event ingestion
  │   ├── models/             # Pydantic models
  │   ├── utils/              # logs, helpers
  │   └── config/             # env, firebase setup
  ├── requirements.txt
  └── Dockerfile

---

# 🧪 Running Locally

## Frontend

cd frontend
npm install
npm run dev


## Backend

cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

---

# 🌐 Deployment (Google Cloud)
- Build Docker image  
- Deploy backend → Cloud Run  
- Configure environment variables  
- Connect Firebase & Firestore  
- Connect Next.js frontend to backend URL  

---

Team 42X007
