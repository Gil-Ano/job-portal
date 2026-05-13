from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/register", response_model=schemas.UserResponse)
def register(user_data: schemas.UserRegister, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    user = models.User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role=user_data.role,
        full_name=user_data.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create profile based on role
    if user_data.role == "employer":
        profile = models.EmployerProfile(user_id=user.id, company_name=user_data.full_name)
    else:
        profile = models.JobseekerProfile(user_id=user.id)

    db.add(profile)
    db.commit()

    return user


@router.post("/login")
def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    # Find user
    user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Verify password
    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Create token
    token = create_access_token({"user_id": user.id})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "full_name": user.full_name,
        }
    }