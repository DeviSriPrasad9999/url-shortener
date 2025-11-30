from pydantic import BaseModel
from fastapi import FastAPI
from .generator import generate_code
from .repository import URLRepository

app = FastAPI()

class ShortenRequest(BaseModel):
    url: str

@app.post("/shorten/")
def shorten_url(request: ShortenRequest):
    code = generate_code()
    URLRepository.save(code, request.url)
    return {"short_code": code}    