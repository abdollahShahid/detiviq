from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.db.deps import get_db
from app.models.organization import Organization
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest

router = APIRouter()


@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    try:
        hashed = hash_password(payload.password)

        org = Organization(name=payload.org_name)
        db.add(org)
        db.flush()

        user = User(
            email=payload.email,
            hashed_password=hashed,
            organization_id=org.id,
        )
        db.add(user)

        db.commit()
        db.refresh(org)
        db.refresh(user)

        return {
            "message": "user created",
            "user_id": user.id,
            "organization_id": org.id,
        }
    except Exception:
        db.rollback()
        raise


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email, "user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}
