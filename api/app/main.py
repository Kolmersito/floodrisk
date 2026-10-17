from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import initialize, fetch_all
from .routes import counties, history, predictions, geography


@asynccontextmanager
async def lifespan(app):
    initialize()
    yield


app = FastAPI(title="FloodRisk API", version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
                   allow_origin_regex=r"http://(localhost|127\.0\.0\.1):517\d",
                   allow_methods=["GET"], allow_headers=["*"])
for module in (counties, predictions, history, geography):
    app.include_router(module.router, prefix="/api")


@app.get("/health")
def health():
    count = fetch_all("SELECT COUNT(*) AS n FROM predictions WHERE json_extract(payload, '$.is_demo') = 0")[0]["n"]
    return {"status": "ok", "model_status": "experimental_predictions_loaded" if count else "no_trained_predictions",
            "trained_prediction_count": count}
