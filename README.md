# Multimodal Construction Intelligence Platform

A full-stack decision-support system for construction professionals.
**React.js (Vite) frontend + FastAPI backend + multimodal LLM**, with strict JSON data contracts (Pydantic) between every layer.

## Modules (one per Epic)
| Module | Endpoint | Input |
|---|---|---|
| Construction site safety monitoring | `POST /api/safety/analyze` | site photo |
| Crack detection and analysis | `POST /api/cracks/analyze` | photo of crack |
| Real estate valuation | `POST /api/valuation` | property details (JSON) |
| Construction project planning | `POST /api/planning` | project brief (JSON) |
| Daily site assistance | `POST /api/assistant/daily` | tasks, crew, optional location |
| Weather-aware advisory | `POST /api/advisory/weather` | lat/lon + activity |
| Construction knowledge assistant | `POST /api/knowledge/ask` | question + history |

Interactive API docs: http://localhost:8000/docs

## Run it

### 1. Backend (Python 3.10+)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # already provided; edit it to choose an AI provider
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend (Node 18+)
```bash
cd frontend
npm install
npm run dev                 # http://localhost:5173
```

## AI provider
Set `LLM_PROVIDER` in `backend/.env`:
- `mock` (default): sample responses, no key needed. Good for demos and UI work.
- `anthropic`: set `ANTHROPIC_API_KEY` (model in `ANTHROPIC_MODEL`).
- `gemini`: set `GEMINI_API_KEY` (model in `GEMINI_MODEL`), which suits the Google Cloud course track.

Restart the backend after editing `.env`.

## How the strict JSON contract works
1. `backend/app/schemas.py` defines every request and response shape.
2. `backend/app/llm.py` sends the JSON schema to the model, extracts the JSON reply, validates it, and retries once with the error if it is invalid.
3. FastAPI `response_model` guarantees the frontend only ever receives validated data.

The weather advisory also applies deterministic rules (strong wind, thunderstorm, hail → `halt`), so the AI can never be more lenient than the safety floor.

## Tests
```bash
cd backend && pytest
```

## Project layout
```
backend/app/   main.py, config.py, schemas.py, llm.py, weather.py, mocks.py, routers/
backend/tests/ test_api.py
frontend/src/  App.jsx, api.js, pages/, components/
```

## Notes
- Valuation and crack/safety outputs are decision support, not certified reports. Have a licensed valuer, structural engineer or safety officer confirm anything critical.
- Weather data comes from Open-Meteo (free, no key).
