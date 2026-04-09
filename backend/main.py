import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from prometheus_fastapi_instrumentator import Instrumentator

from backend.api.predict import router as predict_router
from backend.core.exceptions import global_exception_handler
from backend.core.logging import logger

app = FastAPI(title="AI Prediction API", version="1.0.0")

# Exception handler
app.add_exception_handler(Exception, global_exception_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
Instrumentator().instrument(app).reveal_metrics().expose(app)

# Include Routers
app.include_router(predict_router, prefix="/api")

# Mount static frontend
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend'))
os.makedirs(frontend_dir, exist_ok=True)
if not os.path.exists(os.path.join(frontend_dir, 'index.html')):
    with open(os.path.join(frontend_dir, 'index.html'), 'w') as f:
        f.write("<h1>Loading AI Prediction System...</h1>")

app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up AI Prediction API")

