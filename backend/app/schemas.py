from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ---------- USER SCHEMAS ----------
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: str
    full_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    full_name: str

    class Config:
        from_attributes = True


# ---------- JOB SCHEMAS ----------
class JobCreate(BaseModel):
    title: str
    location: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    description: str
    requirements: Optional[str] = None
    type: str
    category: Optional[str] = None
    deadline: Optional[datetime] = None


class JobResponse(BaseModel):
    id: int
    employer_id: int
    title: str
    company: str
    location: str
    salary_min: Optional[int]
    salary_max: Optional[int]
    description: str
    requirements: Optional[str]
    type: str
    category: Optional[str]
    deadline: Optional[datetime]
    created_at: datetime
    match_score: Optional[float] = None

    class Config:
        from_attributes = True


# ---------- APPLICATION SCHEMAS ----------
class ApplicationCreate(BaseModel):
    job_id: int
    cover_letter: Optional[str] = None


class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    applicant_id: int
    status: str
    match_score: Optional[float]
    cover_letter: Optional[str]
    applied_at: datetime

    class Config:
        from_attributes = True


# ---------- PROFILE SCHEMAS ----------
class EmployerProfileUpdate(BaseModel):
    company_name: Optional[str] = None
    company_description: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None


class JobseekerProfileUpdate(BaseModel):
    headline: Optional[str] = None
    skills: Optional[List[str]] = None


class Token(BaseModel):
    access_token: str
    token_type: str