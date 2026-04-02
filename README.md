# marketing_helper_be

Backend FastAPI del progetto marketing_helper.

## Responsabilita'

- API core clienti e brand identity
- Static serving upload
- Gateway verso servizio multi-agente

## Endpoint principali

- `GET /api/health`
- `POST /api/agent/invoke`
- `GET/POST/PATCH /api/clients/...`

Swagger: `http://localhost:8000/swagger`

## Variabili ambiente

Vedi `.env.example`.

- `APP_NAME`
- `APP_ENV`
- `POSTGRES_URL`
- `MONGO_URL`
- `MONGO_DB_NAME`
- `ANTHROPIC_API_KEY`
- `AGENT_URL`
- `AGENT_TIMEOUT_SECONDS`

## Run locale

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
