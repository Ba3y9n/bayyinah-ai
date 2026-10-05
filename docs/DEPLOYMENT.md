# Deployment & Environment

Bayyinah AI is designed to be easily deployable in modern serverless environments.

## Deployment Architecture

**Recommended Vercel Services (Monorepo)**
The project contains a `vercel.json` in the root directory that defines two Vercel Services:
- `frontend` (Vite) mapping to `/(.*)`
- `backend` (FastAPI) mapping to `/api/(.*)`

This allows both the UI and the API to share a single domain, eliminating CORS issues and hiding backend endpoints behind the Vercel edge network.

## Environment Variables

> **WARNING:** Never commit actual values to Git. Use the `.env.example` as a template.

| Variable                  | Service  | Required    | Secret | Description |
| ------------------------- | -------- | ----------- | ------ | ----------- |
| `GEMINI_API_KEY`          | Backend  | Yes         | Yes    | Gemini API token for extraction and grounding |
| `DATABASE_URL`            | Backend  | Production  | Yes    | PostgreSQL connection string for pgvector |
| `SUPABASE_URL`            | Backend  | Yes         | No     | Supabase instance URL |
| `SUPABASE_ANON_KEY`       | Backend  | Yes         | No     | Supabase public anon key |
| `SUPABASE_SERVICE_ROLE_KEY` | Backend | If enabled  | Yes    | Admin bypass for database management |
| `SERPAPI_API_KEY`         | Backend  | If enabled  | Yes    | Discovery fallback tool |
| `VITE_API_BASE_URL`       | Frontend | Yes         | No     | Points to `/api` or the explicit backend URL |

## Frontend vs Backend Separation
- The frontend (`vite`) receives **only** `VITE_API_BASE_URL`.
- No database credentials, AI keys, or service roles are exposed to the browser.
