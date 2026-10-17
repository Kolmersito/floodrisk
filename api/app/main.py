from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import initialize
from .routes import counties, history, predictions


@asynccontextmanager
async def lifespan(app):
    initialize()
    yield


app = FastAPI(title="FloodRisk API", version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
                   allow_methods=["GET"], allow_headers=["*"])
for module in (counties, predictions, history):
    app.include_router(module.router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok", "model_status": "not_trained"}
