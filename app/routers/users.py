from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from app.security.permissions import require_admin

def safe_user(user : User):
  return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at,
    "updated_at": user.updated_at,
}


router = APIRouter(prefix="/users", tags=["Users"])






@router.get("/")
def get_users(current_user: dict = Depends(require_admin), db: Session = Depends(get_db)):
  users = db.query(User).all()

  return {
    "success": True,
    "message": "Users retrieved successfully",
    "data" : [safe_user(user) for user in users] 
  }

@router.get("/{id}")
def get_user_by_id(id: int, current_user : dict = Depends(require_admin), db: Session = Depends(get_db)):
  user = db.query(User).filter(User.id == id).first()
  if not user:
    raise HTTPException(status_code=404, detail="Users not found")
  return {
    "success": True,
    "message": "User retrieved successfully",
    "data": safe_user(user)
  }

@router.patch("/{id}/role")
def update_route(id: int, role : str, current_user: dict = Depends(require_admin), db : Session = Depends(get_db)):

  user = db.query(User).filter(User.id == id).first()
   
  if not user:
    raise HTTPException(status_code=404, detail="Users not found")
  if role not in ["viewer", "technician", "admin"]:
    raise HTTPException(400, detail="Invalid role")
  user.role = role
  db.commit()
  db.refresh(user)
  return {
    "success": True,
    "message": "User role updated successfully",
    "data": safe_user(user),
  }

@router.patch("/{id}/disable")
def disable_user(id :  int, current_user: dict = Depends(require_admin), db: Session = Depends(get_db)):

  user = db.query(User).filter(User.id == id).first()
   
  if not user:
    raise HTTPException(status_code=404, detail="Users not found")
  user.is_active = False
  db.commit()
  db.refresh(user)
  return {
    "success": True,
    "message": "User disabled successfully",
    "data": safe_user(user),
  }

