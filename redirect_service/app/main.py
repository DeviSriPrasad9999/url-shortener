from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse,Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.middleware.cors import CORSMiddleware

from .repository import URLRepository
from .middleware import MetricsMiddleware

app = FastAPI()

app.add_middleware(MetricsMiddleware)

origins = [
    "http://localhost:4200",
    "https://your-production-site.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # Origins that are allowed to make requests
    allow_credentials=True,           # Allow cookies and authentication headers
    allow_methods=["*"],               # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],               # Allow all headers (Content-Type, Authorization, etc.)
)
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/{code}")
def redirect_to_url(code: str):
    record = URLRepository.get(code)

    if not record:
        raise HTTPException(status_code=404, detail="Short code not found")

    return RedirectResponse(record.long_url)

