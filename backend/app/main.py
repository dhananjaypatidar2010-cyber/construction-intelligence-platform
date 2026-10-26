from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import analysis, assistant, planning

app = FastAPI(title="Multimodal Construction Intelligence Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router)
app.include_router(planning.router)
app.include_router(assistant.router)


@app.get("/api/health")
def health():
    return {"status": "ok", "provider": settings.llm_provider}
