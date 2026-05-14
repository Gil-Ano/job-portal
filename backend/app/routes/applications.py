from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user
from app.services.matching import calculate_match_score
from pypdf import PdfReader
import io

router = APIRouter(prefix="/api/applications", tags=["applications"])


# ----- JOBSEEKER: Apply to a job -----
@router.post("/", response_model=schemas.ApplicationResponse)
def apply_to_job(
    application_data: schemas.ApplicationCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
):
    # Check if user is a jobseeker
    user = db.query(models.User).filter(models.User.id == current_user_id).first()
    if user.role != "jobseeker":
        raise HTTPException(status_code=403, detail="Only jobseekers can apply")

    # Check if job exists
    job = db.query(models.Job).filter(models.Job.id == application_data.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Get jobseeker profile
    seeker = db.query(models.JobseekerProfile).filter(
        models.JobseekerProfile.user_id == current_user_id
    ).first()

    # Check if already applied
    existing = db.query(models.Application).filter(
        models.Application.job_id == application_data.job_id,
        models.Application.applicant_id == seeker.id,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="You already applied to this job")

    # Calculate AI match score if CV exists
    match_score = None
    if seeker.cv_text:
        match_score = calculate_match_score(seeker.cv_text, job.description)

    application = models.Application(
        job_id=application_data.job_id,
        applicant_id=seeker.id,
        cover_letter=application_data.cover_letter,
        match_score=match_score,
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


# ----- JOBSEEKER: View my applications -----
@router.get("/my")
def get_my_applications(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
):
    seeker = db.query(models.JobseekerProfile).filter(
        models.JobseekerProfile.user_id == current_user_id
    ).first()
    if not seeker:
        raise HTTPException(status_code=404, detail="Profile not found")

    applications = (
        db.query(models.Application)
        .filter(models.Application.applicant_id == seeker.id)
        .order_by(models.Application.applied_at.desc())
        .all()
    )

    result = []
    for app in applications:
        job = db.query(models.Job).filter(models.Job.id == app.job_id).first()
        result.append({
            "id": app.id,
            "job_id": app.job_id,
            "job_title": job.title,
            "company": job.company,
            "status": app.status,
            "match_score": app.match_score,
            "cover_letter": app.cover_letter,
            "applied_at": app.applied_at,
        })

    return result


# ----- EMPLOYER: View applications for my jobs -----
@router.get("/received")
def get_received_applications(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
):
    employer = db.query(models.EmployerProfile).filter(
        models.EmployerProfile.user_id == current_user_id
    ).first()
    if not employer:
        raise HTTPException(status_code=403, detail="Employer profile not found")

    # Get all jobs by this employer
    jobs = db.query(models.Job).filter(models.Job.employer_id == employer.id).all()
    job_ids = [j.id for j in jobs]

    applications = (
        db.query(models.Application)
        .filter(models.Application.job_id.in_(job_ids))
        .order_by(models.Application.applied_at.desc())
        .all()
    )

    result = []
    for app in applications:
        job = db.query(models.Job).filter(models.Job.id == app.job_id).first()
        seeker = db.query(models.JobseekerProfile).filter(
            models.JobseekerProfile.id == app.applicant_id
        ).first()
        user = db.query(models.User).filter(models.User.id == seeker.user_id).first()
        result.append({
            "id": app.id,
            "job_id": app.job_id,
            "job_title": job.title,
            "applicant_name": user.full_name,
            "applicant_email": user.email,
            "status": app.status,
            "match_score": app.match_score,
            "cover_letter": app.cover_letter,
            "applied_at": app.applied_at,
        })

    return result


# ----- EMPLOYER: Update application status -----
@router.put("/{application_id}/status")
def update_application_status(
    application_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
):
    if status not in ["applied", "reviewed", "shortlisted", "rejected", "accepted"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    application = db.query(models.Application).filter(
        models.Application.id == application_id
    ).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    # Check ownership (employer owns the job)
    job = db.query(models.Job).filter(models.Job.id == application.job_id).first()
    employer = db.query(models.EmployerProfile).filter(
        models.EmployerProfile.user_id == current_user_id
    ).first()
    if not employer or job.employer_id != employer.id:
        raise HTTPException(status_code=403, detail="Not your job")

    application.status = status
    db.commit()
    return {"message": f"Application status updated to {status}"}


# ----- JOBSEEKER: Upload CV -----
@router.post("/upload-cv")
async def upload_cv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    # Extract text from PDF
    contents = await file.read()
    pdf_file = io.BytesIO(contents)
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    # Save to profile
    seeker = db.query(models.JobseekerProfile).filter(
        models.JobseekerProfile.user_id == current_user_id
    ).first()
    if not seeker:
        raise HTTPException(status_code=404, detail="Profile not found")

    seeker.cv_filename = file.filename
    seeker.cv_text = text
    db.commit()

    return {
        "message": "CV uploaded successfully",
        "filename": file.filename,
        "text_preview": text[:200] + "..."
    }