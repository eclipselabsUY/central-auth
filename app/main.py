from fastapi import FastAPI 
from fastapi.responses import RedirectResponse

from app.auth import auth_router

app = FastAPI()

app.add_api_route(auth_router)


@app.get("/")
def root():
    return RedirectResponse("https://www.ego-services.com")

@app.get("/health")
def health_point():
    return {"status" : "healthy"}