from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.upload import router as upload_router

from api.health import router as health_router
from utils.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Enterprise RAG Chatbot Backend",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Allow Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register Routers
app.include_router(health_router)
app.include_router(upload_router)


@app.get("/")
async def root():
    return {
        "message": "Enterprise RAG Chatbot Backend",
        "version": settings.APP_VERSION
    }