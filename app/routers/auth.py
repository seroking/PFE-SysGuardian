from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserLogin
from app.models.user import User
from  app.security.auth import hash_password, verify_password, create_access_token, verify_token
from fastapi.security import OAuth2PasswordBearer 
#from app.security.permissions import require_admin
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password= hash_password(user.password),
        role="viewer",
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "success": True,
        "message": "User created successfully",
        "data": {
            "id": new_user.id,
            "full_name": new_user.full_name,
            "email": new_user.email,
            "role": new_user.role,
            "is_active": new_user.is_active
        }
    }

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)) :
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user and verify_password(user.password, existing_user.hashed_password):
        token = create_access_token({"sub": existing_user.email, "role": existing_user.role})
        return {
            "success": True,
            "message": "User connected successfully",
            "data":{
                "access_token": token,
                "token_type": "bearer"
            }
        }
    else:
        raise HTTPException(status_code=401, detail="Email or Password incorrect")
        

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
def get_current_user(token: str = Depends(oauth2_scheme)):

    user = verify_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.get("/me")
def me(current_user : dict = Depends(get_current_user)):
    return{
        "success": True,
        "message": "Current user retrieved successfully",
        "data": current_user
    }

