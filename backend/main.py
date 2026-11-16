import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .auth import router as auth_router
from .database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Learning Forex Academy API", version="0.2.0", lifespan=lifespan)
origins = [item.strip() for item in os.getenv("CORS_ORIGINS", os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")).split(",") if item.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["GET","POST","OPTIONS"], allow_headers=["Authorization","Content-Type"])
app.include_router(auth_router)

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "Learning Forex Academy API", "version": "0.2.0"}

@app.get("/")
async def root():
    return {"message": "Learning Forex Academy API"}
