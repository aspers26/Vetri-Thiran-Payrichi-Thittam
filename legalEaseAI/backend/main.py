import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.dependencies import get_settings
from backend.routes import router

settings = get_settings()

app = FastAPI(
    title="LegalEaseAI",
    version="1.0.0",
    description="AI-powered legal document drafting and export API."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "LegalEaseAI Backend Running!"}