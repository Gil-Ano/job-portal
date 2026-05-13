from sqlalchemy import Column, String, Integer, Float, DateTime, Text, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from datetime import datetime, timezone


class UserRole(str, enum.Enum):
    EMPLOYER = "employer"
    JOBSEEKER = "jobseeker"


class ApplicationStatus(str, enum.Enum):
    APPLIED = "applied"
    REVIEWED = "reviewed"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"
    ACCEPTED = "accepted"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    employer_profile = relationship("EmployerProfile", back_populates="user", uselist=False)
    jobseeker_profile = relationship("JobseekerProfile", back_populates="user", uselist=False)


class EmployerProfile(Base):
    __tablename__ = "employer_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    company_name = Column(String, nullable=False)
    company_logo = Column(String, nullable=True)
    company_description = Column(Text, nullable=True)
    website = Column(String, nullable=True)
    location = Column(String, nullable=True)

    user = relationship("User", back_populates="employer_profile")
    jobs = relationship("Job", back_populates="employer")


class JobseekerProfile(Base):
    __tablename__ = "jobseeker_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    headline = Column(String, nullable=True)
    skills = Column(ARRAY(String), default=[])
    cv_filename = Column(String, nullable=True)
    cv_text = Column(Text, nullable=True)

    user = relationship("User", back_populates="jobseeker_profile")
    applications = relationship("Application", back_populates="applicant")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    employer_id = Column(Integer, ForeignKey("employer_profiles.id"))
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, nullable=False)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=True)
    type = Column(String, nullable=False)
    category = Column(String, nullable=True)
    deadline = Column(DateTime, nullable=True)
    is_active = Column(String, default="true")
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    employer = relationship("EmployerProfile", back_populates="jobs")
    applications = relationship("Application", back_populates="job")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    applicant_id = Column(Integer, ForeignKey("jobseeker_profiles.id"))
    status = Column(String, default="applied")
    match_score = Column(Float, nullable=True)
    cover_letter = Column(Text, nullable=True)
    applied_at = Column(DateTime, default=datetime.now(timezone.utc))

    job = relationship("Job", back_populates="applications")
    applicant = relationship("JobseekerProfile", back_populates="applications")


class SavedJob(Base):
    __tablename__ = "saved_jobs"

    id = Column(Integer, primary_key=True, index=True)
    jobseeker_id = Column(Integer, ForeignKey("jobseeker_profiles.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    saved_at = Column(DateTime, default=datetime.now(timezone.utc))