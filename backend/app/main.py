from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app import models
from app.routes import users, jobs, applications

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Portal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://job-portal-wheat-ten.vercel.app", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(jobs.router)
app.include_router(applications.router)


@app.get("/")
def root():
    return {"message": "Get Hired API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}