from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


# ----- EMPLOYER: Create a job -----
@router.post("/", response_model=schemas.JobResponse)
def create_job(
    job_data: schemas.JobCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
):
    # Check if user is an employer
    user = db.query(models.User).filter(models.User.id == current_user_id).first()
    if user.role != "employer":
        raise HTTPException(status_code=403, detail="Only employers can post jobs")

    # Get employer profile
    employer = db.query(models.EmployerProfile).filter(
        models.EmployerProfile.user_id == current_user_id
    ).first()

    job = models.Job(
        employer_id=employer.id,
        title=job_data.title,
        company=employer.company_name,
        location=job_data.location,
        salary_min=job_data.salary_min,
        salary_max=job_data.salary_max,
        description=job_data.description,
        requirements=job_data.requirements,
        type=job_data.type,
        category=job_data.category,
        deadline=job_data.deadline,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


# ----- PUBLIC: Get all jobs with filters -----
@router.get("/")
def get_jobs(
    search: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    salary_min: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(models.Job)

    if search:
        query = query.filter(
            (models.Job.title.ilike(f"%{search}%"))
            | (models.Job.description.ilike(f"%{search}%"))
            | (models.Job.company.ilike(f"%{search}%"))
        )
    if location:
        query = query.filter(models.Job.location.ilike(f"%{location}%"))
    if type:
        query = query.filter(models.Job.type == type)
    if category:
        query = query.filter(models.Job.category == category)
    if salary_min is not None:
        query = query.filter(models.Job.salary_min >= salary_min)

    jobs = query.order_by(models.Job.created_at.desc()).all()
    return jobs


# ----- PUBLIC: Get single job -----
@router.get("/{job_id}", response_model=schemas.JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


# ----- EMPLOYER: Update job -----
@router.put("/{job_id}", response_model=schemas.JobResponse)
def update_job(
    job_id: int,
    job_data: schemas.JobCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Check ownership
    employer = db.query(models.EmployerProfile).filter(
        models.EmployerProfile.user_id == current_user_id
    ).first()
    if not employer or job.employer_id != employer.id:
        raise HTTPException(status_code=403, detail="Not your job listing")

    job.title = job_data.title
    job.location = job_data.location
    job.salary_min = job_data.salary_min
    job.salary_max = job_data.salary_max
    job.description = job_data.description
    job.requirements = job_data.requirements
    job.type = job_data.type
    job.category = job_data.category
    job.deadline = job_data.deadline

    db.commit()
    db.refresh(job)
    return job


# ----- EMPLOYER: Delete job -----
@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    employer = db.query(models.EmployerProfile).filter(
        models.EmployerProfile.user_id == current_user_id
    ).first()
    if not employer or job.employer_id != employer.id:
        raise HTTPException(status_code=403, detail="Not your job listing")

    db.delete(job)
    db.commit()
    return {"message": "Job deleted"}