# CrediLens API Documentation

Base URL: `http://localhost:8000/api`

All JSON endpoints return the standard envelope structure:
```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

On error:
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "INVALID_INPUT",
    "message": "Human-readable description of error."
  }
}
```

---

## 1. System & Health

### `GET /api/health`
Checks server liveness.
- **Auth**: None
- **Response**: `{ "status": "ok", "app": "CrediLens", "version": "1.0.0" }`

### `GET /api/system/status`
Returns live subsystem status booleans.
- **Auth**: None
- **Response**:
```json
{
  "api": true,
  "database": true,
  "models": true,
  "nlp": true,
  "evidence": true,
  "searchKeyConfigured": false
}
```

---

## 2. Authentication

### `POST /api/auth/register`
Register a new user account.
- **Body**:
```json
{
  "email": "user@domain.com",
  "password": "securepassword",
  "displayName": "Full Name"
}
```
- **Response**: `{ "token": "jwt_token", "user": { "id": "...", "email": "...", ... } }`

### `POST /api/auth/login`
Authenticate with email and password.
- **Body**: `{ "email": "...", "password": "..." }`
- **Response**: `{ "token": "jwt_token", "user": { ... } }`

### `GET /api/auth/me`
Retrieve the current authenticated user's profile and preferences.
- **Auth**: `Bearer <token>`

### `PATCH /api/auth/me`
Update profile display name or user preferences.
- **Auth**: `Bearer <token>`
- **Body**: `{ "displayName": "New Name", "preferences": { "theme": "dark", "maxClaims": 8 } }`

---

## 3. Analysis

### `POST /api/analyze/text`
Direct news article / claim text analysis.
- **Auth**: Optional (`Bearer <token>` to link with user account)
- **Body**:
```json
{
  "text": "Full article body or claim assertion text...",
  "title": "Optional headline"
}
```
- **Response**: Full `AnalysisResponse` object.

### `POST /api/analyze/url`
Fetches the article from the specified URL and runs analysis.
- **Auth**: Optional
- **Body**: `{ "url": "https://example.com/article" }`

### `POST /api/analyze/file`
Uploads document file (`.txt`, `.md`, `.pdf`, max 5MB).
- **Auth**: Optional
- **Body**: `multipart/form-data` with `file`

### `GET /api/analyze/{analysis_id}/events`
Server-Sent Events (SSE) progress stream.
- **Output format**: `data: {"stage": "extracting_claims", "label": "...", "done": true}\n\n`
- Stages:
  1. `extracting_article`
  2. `analyzing_text`
  3. `extracting_claims`
  4. `searching_evidence`
  5. `evaluating_sources`
  6. `calculating_credibility`
  7. `generating_explanation`
  8. `completed`

---

## 4. History & Reports

### `GET /api/analysis/history`
Query paginated analysis history.
- **Query Params**:
  - `q`: Search keyword
  - `sort`: `createdAt_desc` | `createdAt_asc`
  - `page`: Integer (default 1)
  - `limit`: Integer (default 20)

### `GET /api/analysis/{analysis_id}`
Retrieve a saved analysis by ID.

### `DELETE /api/analysis/{analysis_id}`
Delete a saved analysis document.

### `GET /api/analysis/{analysis_id}/report`
Generate printable / downloadable report structure.
