from pydantic import BaseModel
from fastapi import FastAPI
from .generator import generate_code
from .repository import URLRepository
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class ShortenRequest(BaseModel):
    url: str

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

@app.post("/shorten/")
def shorten_url(request: ShortenRequest):
    code = generate_code()
    URLRepository.save(code, request.url)
    return {"short_code": code}    