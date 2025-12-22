# MARGSATHI Mobility Intelligence – Backend

FastAPI backend for the **MARGSATHI** mobility intelligence platform.  
API-first, modular, and hackathon-ready.

## Tech stack

- FastAPI (Python)
- Uvicorn ASGI server
- Pydantic models

## Project layout

- `backend/main.py` – application factory, FastAPI app, router wiring
- `backend/routes/routing.py` – route planning APIs
- `backend/routes/parking.py` – parking discovery APIs
- `backend/routes/events.py` – mobility-impacting events APIs
- `backend/routes/translation.py` – mock translation APIs

## Setup

1. Create a virtual environment (recommended):

   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # On Windows PowerShell: .venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server from the project root:

   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. Open the interactive API docs:

   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## Key endpoints (overview)

- `GET /` – API metadata + basic status
- `GET /health` – simple health check
- `POST /api/routing/plan` – plan a simple route between two coordinates
- `GET /api/parking/search` – search for nearby parking (mock data)
- `GET /api/events/nearby` – fetch mobility-impacting events (mock data)
- `POST /api/translation/simple` – mocked translation helper

All feature endpoints are intentionally lightweight and in-memory so you can
quickly iterate during hackathons and later plug in real data sources or services.


