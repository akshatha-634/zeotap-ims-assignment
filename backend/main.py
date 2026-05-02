from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.signals import router as signal_router
import asyncio
import time

app = FastAPI(title="Incident Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(signal_router, prefix="/api")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "IMS Backend Running"}
