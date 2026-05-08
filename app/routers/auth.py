from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import user as crud_user
from app.database import get_db
from app.schemas.auth import AuthResponse, UserCreate, UserLogin
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_username = crud_user.get_user_by_username(db, user.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already registered")

    existing_email = crud_user.get_user_by_email(db, user.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = crud_user.create_user(
        db=db,
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
    )
    token, expires_at = create_access_token(db_user.id)
    return {"access_token": token, "expires_at": expires_at, "user": db_user}


@router.post("/login", response_model=AuthResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_username(db, credentials.username)
    if not db_user or not verify_password(credentials.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token, expires_at = create_access_token(db_user.id)
    return {"access_token": token, "expires_at": expires_at, "user": db_user}
