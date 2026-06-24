from fastapi import HTTPException, Depends
from app.routers.auth import get_current_user

def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
 

def require_technician(current_user : dict = Depends(get_current_user)):
    if current_user["role"] != "technician" and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Technician access required")
    return current_user