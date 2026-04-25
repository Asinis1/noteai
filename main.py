from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from backend.database import engine, Base
from backend.routes import auth, notes, ai


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Akıllı Not Alma Sistemi",
    description="AI destekli not alma, özetleme ve etiketleme API'si",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(ai.router)


@app.get("/")
def root():
    return {"message": "Akıllı Not Alma Sistemi API'ye hoş geldiniz!", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}