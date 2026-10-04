<<<<<<< HEAD
# CrediLens — AI-Powered Misinformation and Fake News Credibility Analyzer

![CrediLens Dashboard Reference](docs/ui_preview.png)

CrediLens is an end-to-end full-stack intelligence dashboard that analyzes news articles, claims, and documents to generate a transparent, multi-factor **Credibility Assessment**.

---

## 1. System Architecture

```
USER INPUT (Text / URL / Document)
    │
    ▼
FastAPI Application Orchestrator
    ├── Article Extraction (trafilatura / bs4 / pypdf)
    ├── NLP Pipeline & Entity Recognition
    ├── Factual Claim Extraction
    ├── AI/ML Classification (TF-IDF + Calibrated Logistic Regression / DistilBERT)
    ├── Evidence Retrieval (Wikipedia API + Multi-provider Web Search)
    ├── Semantic Relevance Ranking & Stance Classification
    ├── Source Transparency Analysis
    ├── Language & Sensationalism Analysis
    ├── Multi-Factor Credibility Scoring Engine (0–100)
    └── Explainability & Key Findings Synthesis
    │
    ▼
MongoDB Atlas Persistence (Denormalized History)
    │
    ▼
React + Tailwind + Recharts Dashboard (Desktop & Mobile)
```

---

## 2. Core Features

- **Multi-Modal Input**: Paste raw article text, enter web article URLs, or upload `.txt`, `.md`, `.pdf` documents.
- **Real-Time Progress**: Live Server-Sent Events (SSE) stream backend analysis stages sequentially.
- **Credibility Assessment (0–100)**: Transparent weighted score combining:
  - AI Classification (30%)
  - Evidence Verification (30%)
  - Source Transparency (20%)
  - Language / Sensationalism (10%)
  - Claim Consistency (10%)
- **Factual Claim Verification**: Categorizes extracted claims into `SUPPORTED`, `CONTRADICTED`, or `INSUFFICIENT_EVIDENCE` (missing evidence is never labeled "false").
- **Source Transparency**: Evaluates author presence, timestamps, domain quality, publisher identity, and citation links.
- **Linguistic Analysis**: Detects emotional charge, clickbait markers, excessive punctuation, and absolute assertions.
- **Explainable AI**: Model n-gram feature importance combined with structured Key Findings.
- **Analysis History & Reports**: Filterable history, detailed deep-links, and exportable printable reports.
- **Authentication**: JWT authentication with demo seed user (`demo@credilens.local` / `demo1234`).

---

## 3. Technology Stack

- **Frontend**: React 19, Tailwind CSS, Recharts, Lucide React, Axios, Vite
- **Backend**: Python 3.11+, FastAPI, Uvicorn, Pydantic v2
- **ML / NLP**: scikit-learn, joblib, transformers, NumPy, pandas, trafilatura, beautifulsoup4
- **Database**: MongoDB (Motor async client) with resilient in-memory fallback
- **Evidence**: Wikipedia OpenSearch API, DuckDuckGo search, Tavily/Serper integration

---

## 4. Quick Start (Local Development)

### Backend Setup
```bash
# 1. Install backend dependencies
pip install -r backend/requirements.txt

# 2. Train baseline model artifacts (persists to ml/saved_models/)
python ml/training/train_baselines.py

# 3. Start FastAPI server (runs at http://localhost:8000)
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Frontend Setup
```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Start Vite dev server (runs at http://localhost:5173)
npm run dev
```

### Run Tests
```bash
# Backend pytest suite (NLP, ML, Scoring, API tests)
python -m pytest backend/tests/ -v

# Frontend build check
cd frontend && npm run build
```

---

## 5. Documentation

- [API Specification](docs/API.md)
- [Scoring Methodology](docs/SCORING.md)
- [System Architecture](docs/ARCHITECTURE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [ML Evaluation Metrics](ml/evaluation/METRICS.md)

---

## 6. Scientific Disclaimer

> This assessment estimates credibility using AI classification, evidence retrieval, source analysis, and linguistic signals. It is not a determination of absolute truth.
=======
# credilens-ai-news-analyzer
AI-powered news credibility analyzer that uses NLP, machine learning, and source analysis to detect potential misinformation and provide explainable credibility scores.
>>>>>>> b81cb1203979fa4da5a942c5ae593c7fa4d02dd6
