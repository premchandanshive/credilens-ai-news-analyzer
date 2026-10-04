# CrediLens — Architecture & Implementation Plan (Model 1)

**Product name:** CrediLens (AI News Analyzer)  
**Academic title:** AI-Powered Misinformation and Fake News Credibility Analyzer  
**Status:** Architecture only. No application implementation until this plan is followed by Models 2–8.  
**Workspace inspection (2026-08-20):** empty project root. Greenfield build.

This document is the **single source of truth** for subsequent stages. Do not invent parallel architectures.

---

## 1. Scientific framing (non-negotiable)

CrediLens estimates **credibility**, not absolute truth.

The UI and API copy must state:

> This assessment estimates credibility using AI classification, evidence retrieval, source analysis, and linguistic signals. It is not a determination of absolute truth.

Distinguish:

| Signal | Meaning |
|--------|---------|
| **AI prediction** | Supervised classifier output (likely-fake / likely-real style labels + probability). Linguistic/statistical pattern, not verification. |
| **Evidence verification** | Per-claim status: `SUPPORTED` / `CONTRADICTED` / `INSUFFICIENT_EVIDENCE`. Missing evidence must never become “false”. |

Claim statuses must never include a blanket `FALSE` derived from search failure.

---

## 2. System architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  React (Vite) + Tailwind + Recharts                             │
│  Layout: Sidebar / Topbar / MobileNavbar                         │
│  Pages: Dashboard, Analyze, History, Sources, Reports, Settings │
│  services/: apiClient, analysisService, authService, …          │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS JSON + SSE (analysis progress)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  FastAPI (Uvicorn)                                              │
│  api/ → schemas → services → ml / nlp / evidence / scoring      │
│  JWT auth (optional session for history ownership)              │
└──────┬──────────────┬──────────────┬──────────────┬─────────────┘
       │              │              │              │
       ▼              ▼              ▼              ▼
   MongoDB        ML artifacts    Evidence       External
   Atlas          (joblib +       providers      search APIs
                  DistilBERT)     (interface)    (env keys)
```

**Request-time analysis pipeline (backend orchestration, not training):**

```
Input (text | URL | file)
  → Validation
  → Article extraction (URL/file → plain text)
  → Text cleaning + NLP (spaCy)
  → Claim extraction
  → ML inference (loaded artifacts only)
  → Evidence retrieval + ranking (semantic similarity)
  → Source transparency scoring
  → Language / sensationalism analysis
  → Credibility score engine (weighted, configurable)
  → Explainability (feature importance + evidence-based)
  → Persist analysis in MongoDB
  → Stream progress + return envelope
```

**Hard rule:** training happens only in `ml/training/`. FastAPI loads saved artifacts at startup.

---

## 3. Folder structure

```
project/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/          # reusable UI (see §8)
│   │   ├── layouts/             # AppLayout, AuthLayout
│   │   ├── pages/               # Dashboard, Analyze, History, Sources, Reports, Settings, Auth
│   │   ├── hooks/               # useAnalysis, useAuth, useMediaQuery
│   │   ├── services/            # apiClient, analysisService, historyService, systemService, authService
│   │   ├── context/             # AuthContext, ThemeContext
│   │   ├── types/               # mirrored API contracts
│   │   ├── utils/               # score labels, formatters, validation
│   │   ├── styles/              # index.css + Tailwind tokens
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── vercel.json
│   └── .env.example
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app, CORS, lifespan (load models, DB)
│   │   ├── api/
│   │   │   ├── deps.py          # auth, DB
│   │   │   ├── routes/
│   │   │   │   ├── health.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── analyze.py   # text/url/file + SSE progress
│   │   │   │   ├── analysis.py  # get/list/delete
│   │   │   │   ├── sources.py
│   │   │   │   └── system.py
│   │   ├── core/
│   │   │   ├── config.py        # pydantic-settings
│   │   │   ├── security.py      # JWT, password hashing
│   │   │   ├── errors.py        # envelope errors
│   │   │   └── scoring.py       # weight config (not “proven science”)
│   │   ├── schemas/             # Pydantic request/response
│   │   ├── models/              # Mongo document shapes (TypedDict / dataclasses)
│   │   ├── database/
│   │   │   ├── mongodb.py       # Motor client, indexes
│   │   │   └── repositories.py
│   │   ├── services/
│   │   │   ├── analysis_orchestrator.py
│   │   │   ├── extraction.py    # URL + file → text
│   │   │   ├── auth_service.py
│   │   │   └── report_service.py
│   │   ├── ml/
│   │   │   ├── inference.py     # load once, predict
│   │   │   └── loader.py
│   │   ├── nlp/
│   │   │   ├── pipeline.py      # clean, sentences, NER, phrases
│   │   │   ├── claims.py
│   │   │   └── language.py      # sensationalism / emotion / clickbait
│   │   ├── evidence/
│   │   │   ├── base.py          # EvidenceProvider protocol
│   │   │   ├── wikipedia.py
│   │   │   ├── web_search.py    # Tavily / Serper / DuckDuckGo fallback
│   │   │   ├── ranker.py        # sentence-transformers MiniLM
│   │   │   └── classify.py      # support / contradict / insufficient
│   │   └── explainability/
│   │       ├── lime_explainer.py   # sklearn pipeline when suitable
│   │       ├── feature_importance.py
│   │       └── evidence_reasons.py
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── render.yaml
│   └── .env.example
├── ml/
│   ├── datasets/                # README + small sample; download script (not huge dumps in git)
│   ├── notebooks/
│   ├── training/
│   │   ├── train_baselines.py
│   │   ├── train_transformer.py
│   │   └── evaluate.py
│   ├── evaluation/
│   │   └── METRICS.md           # filled after Model 3 training run
│   └── saved_models/            # gitignored except README; artifacts from training
├── docs/
│   ├── ARCHITECTURE.md          # this file
│   ├── API.md                   # generated/expanded by Model 4
│   ├── SCORING.md               # methodology (weights are configurable, not proven)
│   └── DEPLOYMENT.md            # Model 8
├── .env.example                 # root: points to frontend/backend examples
├── .gitignore
└── README.md                    # Model 8 fills; stub after Model 2/4 as needed
```

Do **not** duplicate the same feature in `frontend/src` and a second “demo” app.

---

## 4. Database schema (MongoDB)

Database name: `credilens` (overridable via `MONGODB_DB`).

### 4.1 `users`

```json
{
  "_id": "ObjectId",
  "email": "string (unique, lowercase)",
  "passwordHash": "string (bcrypt/argon2 — never plaintext)",
  "displayName": "string",
  "role": "student | researcher | admin",
  "preferences": {
    "theme": "dark | light",
    "maxClaims": 8,
    "includeTransformer": true
  },
  "createdAt": "ISODate",
  "updatedAt": "ISODate"
}
```

Indexes: unique `email`.

Guest mode: if unauthenticated, analyses may be stored with `userId: null` and a client `sessionId` (optional). Prefer authenticated history for the academic demo; Model 4 implements JWT + a default demo user seed **without** a hardcoded production password in git.

### 4.2 `analyses` (primary history document)

Store a **denormalized snapshot** of the result so history opens without joining huge graphs. Cap text size (`articleText` truncated to e.g. 50k chars; full text optional in GridFS only if needed — default: truncate).

```json
{
  "_id": "ObjectId",
  "userId": "ObjectId | null",
  "inputType": "text | url | file",
  "inputText": "string | null",
  "inputUrl": "string | null",
  "fileName": "string | null",
  "title": "string",
  "articleExcerpt": "string",
  "prediction": {
    "label": "likely_reliable | likely_unreliable | uncertain",
    "modelName": "string",
    "probabilities": { "reliable": 0.0, "unreliable": 0.0 },
    "aiClassificationScore": 0
  },
  "credibilityScore": 72,
  "credibilityBand": "likely_reliable",
  "disclaimer": "string",
  "componentScores": {
    "aiClassification": 0,
    "evidenceVerification": 0,
    "sourceAnalysis": 0,
    "languageAnalysis": 0,
    "claimConsistency": 0
  },
  "weightsUsed": { "aiClassification": 0.30, "...": "..." },
  "claims": [
    {
      "id": "c1",
      "text": "string",
      "status": "SUPPORTED | CONTRADICTED | INSUFFICIENT_EVIDENCE",
      "confidence": 0.0,
      "evidenceIds": ["..."]
    }
  ],
  "sources": [
    {
      "title": "string",
      "url": "string",
      "domain": "string",
      "publisher": "string | null",
      "author": "string | null",
      "publishedAt": "string | null",
      "excerpt": "string",
      "relevanceScore": 0,
      "transparencyScore": 0,
      "relationship": "supports | contradicts | related | insufficient"
    }
  ],
  "languageAnalysis": {
    "sensationalismScore": 0,
    "emotionalLanguage": "low | moderate | high",
    "clickbaitIndicators": "low | moderate | high",
    "absoluteClaimCount": 0,
    "signals": ["..."]
  },
  "explanation": {
    "findings": [
      { "tone": "positive | warning | negative | info", "text": "string", "basis": "evidence | language | model | source" }
    ],
    "modelExplanation": {
      "method": "lime | feature_importance | unavailable",
      "topFeatures": [{ "feature": "string", "weight": 0.0 }]
    }
  },
  "nlp": {
    "entities": [{ "text": "string", "label": "string" }],
    "claimCount": 0
  },
  "status": "completed | failed | partial",
  "error": { "code": "string", "message": "string" } | null,
  "createdAt": "ISODate",
  "updatedAt": "ISODate"
}
```

Indexes: `userId + createdAt`, `createdAt`, text index on `title` + `articleExcerpt` for search.

### 4.3 `evidence` (cache — avoid duplicate searches)

```json
{
  "_id": "ObjectId",
  "claimHash": "sha256(normalized claim)",
  "query": "string",
  "provider": "wikipedia | tavily | ddg",
  "results": [{ "url": "string", "title": "string", "snippet": "string" }],
  "expiresAt": "ISODate",
  "createdAt": "ISODate"
}
```

Indexes: unique `claimHash + provider`, TTL on `expiresAt`.

### 4.4 `sources` (domain metadata cache)

```json
{
  "_id": "ObjectId",
  "domain": "string (unique)",
  "publisher": "string | null",
  "transparencySignals": {
    "hasAuthorOften": false,
    "notes": "string"
  },
  "updatedAt": "ISODate"
}
```

**Do not** store a hardcoded “BBC = 92 reliable” table as scientific fact. Transparency is computed from **available metadata on that fetch** (author, date, publisher, URL quality, excerpt relevance). Optional curated domain hints may be used as a **weak prior** and must be documented as such in `docs/SCORING.md`.

---

## 5. API specification

Base path: `/api`. All JSON responses use:

```json
{ "success": true, "data": {}, "error": null }
```

```json
{
  "success": false,
  "data": null,
  "error": { "code": "INVALID_INPUT", "message": "Human-readable, no stack trace" }
}
```

Error codes: `INVALID_INPUT`, `UNSUPPORTED_FILE`, `URL_FETCH_FAILED`, `TIMEOUT`, `MODEL_UNAVAILABLE`, `EVIDENCE_UNAVAILABLE`, `DB_UNAVAILABLE`, `UNAUTHORIZED`, `NOT_FOUND`, `PAYLOAD_TOO_LARGE`, `INTERNAL`.

### Endpoints

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| GET | `/api/health` | no | Liveness |
| GET | `/api/system/status` | no | DB, models, NLP, evidence providers, keys present (boolean only) |
| POST | `/api/auth/register` | no | Create user |
| POST | `/api/auth/login` | no | JWT |
| POST | `/api/auth/logout` | yes | Client discards token (stateless JWT) |
| GET | `/api/auth/me` | yes | Profile + preferences |
| PATCH | `/api/auth/me` | yes | Display name, preferences, theme |
| POST | `/api/analyze/text` | optional | Body: `{ text, title? }` |
| POST | `/api/analyze/url` | optional | Body: `{ url }` |
| POST | `/api/analyze/file` | optional | Multipart file (txt, md, pdf if practical) |
| GET | `/api/analyze/{id}/events` | optional | SSE progress for in-flight job (or poll) |
| GET | `/api/analysis/history` | optional | Query: `q`, `sort`, `from`, `to`, `page`, `limit` |
| GET | `/api/analysis/{id}` | optional | Full analysis |
| DELETE | `/api/analysis/{id}` | owner | Delete |
| GET | `/api/analysis/{id}/report` | optional | JSON report payload (frontend prints/downloads) |
| GET | `/api/sources/{id}` | optional | Source detail if split; else embedded in analysis |

**Progress (do not fake on the frontend):**

Prefer **SSE** from `POST /api/analyze/*` returning `analysisId` immediately then events, **or** a two-step `POST` that starts a job + `GET .../events`.

Event payload example:

```json
{ "stage": "extracting_article", "label": "Extracting article...", "done": false }
```

Stages (backend-emitted only when that step starts/completes):

1. `extracting_article`
2. `analyzing_text`
3. `extracting_claims`
4. `searching_evidence`
5. `evaluating_sources`
6. `calculating_credibility`
7. `generating_explanation`
8. `completed` | `failed`

**Analyze response `data` (completed):** same shape as `analyses` document (JSON-serializable; `_id` as `id` string).

Limits: text 50_000 chars; file 5 MB; URL must be `http/https`; timeout 60s orchestrator with per-provider timeouts.

---

## 6. ML / NLP pipeline

### 6.1 Datasets (Model 3)

- Primary training: public fake-news corpus (e.g. WELFake / ISOT / LIAR for claims). Prefer one well-documented news-article dataset for the article classifier.
- Keep **sample CSV** in-repo (tiny) so tests run without download.
- Download script with checksum notes; do not commit multi-GB data.

### 6.2 Baselines (train offline)

- TF-IDF + Logistic Regression (default sklearn inference if transformer missing)
- TF-IDF + Linear SVM
- Multinomial Naive Bayes (comparison)

Metrics: accuracy, precision, recall, F1, confusion matrix → `ml/evaluation/METRICS.md`.

### 6.3 Transformer

- **DistilBERT** (`distilbert-base-uncased`) sequence classification, max length 256–512.
- Saved under `ml/saved_models/distilbert_credilens/`.
- If GPU/download unavailable: sklearn baseline remains production inference; transformer is optional via `ENABLE_TRANSFORMER=true`.
- FastAPI **never** trains.

### 6.4 NLP (spaCy)

- Model: `en_core_web_sm` (practical).
- Cleaning: whitespace, boilerplate, URL noise.
- Sentence split, NER, noun-chunk phrases.
- Claims: sentence-level heuristic (factual verbs, entities, numbers) + cap N claims (settings `maxClaims`).
- Language: caps ratio, `!/?` density, clickbait lexicons, absolute terms (always/never/completely), fear/urgency lexicons. Output scores — **not** a fake-news verdict.

### 6.5 Evidence

`EvidenceProvider` protocol: `search(query, k) -> list[SearchHit]`.

Providers (priority):

1. Tavily or Serper if `TAVILY_API_KEY` / `SERPER_API_KEY` set
2. Wikipedia API (no key)
3. DuckDuckGo HTML/instant answer fallback (rate-limit, fail open)

Rank with `sentence-transformers/all-MiniLM-L6-v2` cosine similarity vs claim.

Classify:

- high similarity + stance align → `SUPPORTED`
- high similarity + negation/conflict cues → `CONTRADICTED`
- else → `INSUFFICIENT_EVIDENCE`

Never fabricate URLs or snippets.

### 6.6 Scoring engine (`docs/SCORING.md`)

Initial weights (**configurable**, not scientifically proven):

| Component | Weight |
|-----------|--------|
| AI classification | 30% |
| Evidence verification | 30% |
| Source analysis | 20% |
| Language analysis | 10% |
| Claim consistency | 10% |

Bands:

| Score | Band label |
|-------|------------|
| 0–20 | Highly Unreliable |
| 21–40 | Likely Misleading |
| 41–60 | Uncertain |
| 61–80 | Likely Reliable |
| 81–100 | Highly Reliable |

UI label: **Credibility Assessment** (not Absolute Truth Score).

### 6.7 Explainability

- Sklearn path: LIME or coefficient-based top n-grams (real model features).
- Transformer path: if SHAP/LIME too heavy, use attention-agnostic **token/feature importance fallback** plus evidence findings.
- Always attach **evidence-based findings** that match stored claims/sources.

---

## 7. Frontend structure & design system

**Visual reference:** uploaded CrediLens dashboard (dark navy, purple accent, sidebar, gauge, breakdown cards, mobile bottom nav). **Do not** copy sample numbers (72, BBC, Reuters, etc.) as production data.

### Design tokens (Tailwind)

```
bg-app: #0B1020 (approx)
bg-sidebar / bg-card: slightly lighter navy
accent: violet-600 / purple-500
text: zinc-100
muted: zinc-400
success: emerald
warning: amber
danger: rose
info: blue
ai: violet
```

Centralize in `tailwind.config.js` theme.extend.colors (`credilens.*`).

### Routes

| Path | Page |
|------|------|
| `/login`, `/register` | Auth |
| `/` | Dashboard (input + last/latest result or empty state) |
| `/analyze` | Dedicated analyze (same input, full-width) |
| `/history` | Search, filter, sort, open, delete |
| `/sources` | Sources from latest or selected analysis |
| `/reports` | Full report + download (print/JSON/PDF-via-print) |
| `/settings` | Theme, profile, preferences, API/system status |
| `/analysis/:id` | Deep link to a saved analysis (dashboard filled) |

### Component map

| Component | Role |
|-----------|------|
| `Sidebar` | Desktop nav |
| `Topbar` | Title, theme, notifications (real: analysis complete / errors), profile |
| `MobileNavbar` | Bottom: Home, Analyze, History, Sources |
| `AppLayout` | Sidebar + topbar + outlet + mobile nav |
| `AnalysisInput` | Text / URL / file, validation, Analyze CTA |
| `AnalysisProgress` | Backend-driven stages |
| `CredibilityGauge` | 0–100 arc (SVG or Recharts) |
| `ScoreCard` | Breakdown metric |
| `AnalysisBreakdown` | Text / Source / Fact-checking mapped to component scores |
| `KeyFindings` | Explanation findings |
| `SourceCard` / `SourceList` | Linked URLs |
| `ClaimCard` / `ClaimList` | Verification status |
| `EvidenceCard` | Snippet + relationship |
| `HistoryTable` | Desktop table + mobile cards |
| `ReportView` | Printable report |
| `EmptyState` / `ErrorState` / `LoadingState` | Shared |
| Charts | Component comparison bar, claim pie, evidence pie, history line |

**Placeholder policy (Model 2 only):** typed `analysisService` returning empty/error until backend exists. **No** hardcoded 72/BBC. Empty states until Model 6.

---

## 8. Auth & security

- JWT access token (short-lived) + optional refresh later (keep simple: 7-day JWT for academic demo).
- Passwords: bcrypt or argon2.
- CORS from `FRONTEND_ORIGINS`.
- Secrets only in env.
- File: allowlist `txt, md, pdf`; size limit.
- URL: SSRF protections (block localhost/metadata IPs in production config).
- Never send API keys to the client. `/system/status` returns booleans only.

---

## 9. Deployment

| Piece | Target |
|-------|--------|
| Frontend | Vercel (`VITE_API_BASE_URL`) |
| Backend | Render or Railway (Docker or native Python) |
| DB | MongoDB Atlas |
| Models | baked into image or downloaded at build/start from Hub (documented) |

---

## 10. Development phases (Models 2–8)

| Phase | Owner | Scope | Exit criteria |
|-------|-------|-------|----------------|
| **2** | Frontend | Vite+React+Tailwind+Router+Recharts+Lucide, layouts, all pages, design tokens, empty/error/loading, service stubs | `npm run dev` + `npm run build` succeed; UI matches reference; no fake scores |
| **3** | ML/NLP | Datasets sample, train baselines, evaluate, DistilBERT optional, NLP/claims/language, inference module, persist artifacts | Unit tests on clean/predict/claims; no FastAPI required |
| **4** | Backend+DB | FastAPI, Motor, schemas, auth, analyze orchestrator calling ML, persist, CORS, tests | `/api/health`, analyze text without evidence OK (evidence stub) |
| **5** | Evidence | Provider interface, Wikipedia + keyed search + fallback, rank, classify, cache, transparency | Pipeline tests with mocked HTTP |
| **6** | Integration | Wire frontend to APIs, SSE progress, replace stubs, charts from API | E2E text analysis shows real numbers |
| **7** | QA | Fix bugs, invalid inputs, downed Mongo/search/model, mobile/desktop | Build + API tests green |
| **8** | Deploy | README, env examples, Vercel/Render, METRICS docs, limitations | Another developer can run locally |

**Rules for every phase:** inspect existing code; fix broken previous work first; no duplicate features; no secrets; no request-time training; no fake evidence.

---

## 11. Testing strategy

- Backend: pytest for validation, scoring math, claim extraction, inference on fixture text, repository with mongomock or testcontainer if available.
- Frontend: Vitest + React Testing Library for input validation, error/empty, score rendering from **fixtures** (API-shaped, not UI-hardcoded production path).
- Integration: script or pytest hitting running API with `MONGODB_URI` test DB.

---

## 12. Known constraints (planned fallbacks)

- No search API key → Wikipedia + DDG fallback; more `INSUFFICIENT_EVIDENCE`.
- No transformer weights → sklearn TF-IDF pipeline.
- No spaCy model download in CI → skip NER tests or vendor sm model install in docs.
- SHAP on DistilBERT may be too slow → LIME on sklearn + evidence explanations.

---

## 13. Model 1 decision log

1. Product UI name: **CrediLens**; academic name in README.
2. SSE (or job+events) for honest progress.
3. DistilBERT optional; sklearn always available.
4. Evidence behind `EvidenceProvider`; keys in env.
5. JWT auth for owned history; optional guest analyses.
6. Denormalized `analyses` documents for fast history.
7. Scoring weights in config + `docs/SCORING.md` disclaimer.
8. Empty workspace → create structure starting Model 2.

**Next:** Model 2 — Frontend Specialist, following this document and the reference UI image.
