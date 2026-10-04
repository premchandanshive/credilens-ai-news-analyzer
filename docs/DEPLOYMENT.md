# CrediLens — Deployment & Operations Guide

This guide details deployment procedures for the React frontend, FastAPI backend, ML models, and MongoDB Atlas database.

---

## 1. Environment Variables Configuration

### Backend (`backend/.env`)
```bash
APP_NAME=CrediLens
APP_VERSION=1.0.0
DEBUG=false
HOST=0.0.0.0
PORT=8000

# CORS Origins
FRONTEND_ORIGINS=https://credilens.vercel.app,http://localhost:5173

# MongoDB Connection
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB=credilens

# JWT Secret (Generate with openssl rand -hex 32)
JWT_SECRET=your_production_secret_key_here

# Optional Search API Keys
TAVILY_API_KEY=
SERPER_API_KEY=

# Model Configuration
MAX_CLAIMS=6
ENABLE_TRANSFORMER=false
```

### Frontend (`frontend/.env`)
```bash
VITE_API_BASE_URL=https://credilens-api.onrender.com
```

---

## 2. Frontend Deployment (Vercel)

1. Connect your repository to **Vercel**.
2. Set Root Directory to `frontend`.
3. Set Framework Preset to **Vite**.
4. Set Environment Variable: `VITE_API_BASE_URL` to your backend URL.
5. Deploy. (Routing is configured in `frontend/vercel.json`).

---

## 3. Backend Deployment (Render / Railway)

### Using Native Python (Render Web Service)
1. **Root Directory**: `backend`
2. **Build Command**:
   ```bash
   pip install -r requirements.txt && python ../ml/training/train_baselines.py
   ```
3. **Start Command**:
   ```bash
   uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
   ```

### Using Docker
1. Build container:
   ```bash
   docker build -t credilens-backend -f backend/Dockerfile .
   ```
2. Run container:
   ```bash
   docker run -p 8000:8000 --env-file backend/.env credilens-backend
   ```

---

## 4. Database Setup (MongoDB Atlas)

1. Create a free M0 cluster on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Create a database user with read/write privileges on `credilens`.
3. Whitelist Network Access IP (`0.0.0.0/0` or your hosting provider IP range).
4. Copy the connection string into `MONGODB_URI`.
