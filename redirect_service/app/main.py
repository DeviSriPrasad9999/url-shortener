from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse,Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from .repository import URLRepository
from .middleware import MetricsMiddleware

app = FastAPI()

app.add_middleware(MetricsMiddleware)

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/{code}")
def redirect_to_url(code: str):
    record = URLRepository.get(code)

    if not record:
        raise HTTPException(status_code=404, detail="Short code not found")

    return RedirectResponse(record.long_url)

