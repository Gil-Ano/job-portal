from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app import models
from app.routes import users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Portal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Job Portal API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}