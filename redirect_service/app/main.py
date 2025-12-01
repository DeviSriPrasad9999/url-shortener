from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from .repository import URLRepository

app = FastAPI()

@app.get("/{code}")
def redirect_to_url(code: str):
    record = URLRepository.get(code)

    if not record:
        raise HTTPException(status_code=404, detail="Short code not found")

    return RedirectResponse(record.long_url)
