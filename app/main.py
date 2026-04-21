from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.router import auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")


@app.get("/")
def root():
    return RedirectResponse("https://www.eclipselabs.com.uy")


@app.get("/health")
def health_point():
    return {"status": "healthy"}
