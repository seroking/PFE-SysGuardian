from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
import psutil

from app.routers.auth import get_current_user
from app.security.permissions import require_admin, require_technician
from app.services.system_service import (
    get_cpu_data,
    get_memory_data,
    get_storage_data,
    get_summary_data,
    get_processes_data,
    get_ports_data,
    get_services_data,
    kill_process_by_pid,
)

router = APIRouter(prefix="/system", tags=["System"])


@router.get("/storage")
def get_storage(current_user: dict = Depends(get_current_user)):
    return {
        "success": True,
        "message": "Storage information retrieved successfully",
        "timestamp": datetime.now(),
        "data": get_storage_data(),
    }


@router.get("/memory")
def get_memory(current_user: dict = Depends(get_current_user)):
    return {
        "success": True,
        "message": "Memory information retrieved successfully",
        "timestamp": datetime.now(),
        "data": get_memory_data(),
    }


@router.get("/cpu")
def get_cpu(current_user: dict = Depends(get_current_user)):
    return {
        "success": True,
        "message": "CPU information retrieved successfully",
        "timestamp": datetime.now(),
        "data": get_cpu_data(),
    }


@router.get("/summary")
def get_summary(current_user: dict = Depends(get_current_user)):
    return {
        "success": True,
        "message": "System summary retrieved successfully",
        "timestamp": datetime.now(),
        "data": get_summary_data(),
    }


@router.get("/processes")
def get_processes(current_user: dict = Depends(require_technician)):
    return {
        "success": True,
        "message": "Processes information retrieved successfully",
        "timestamp": datetime.now(),
        "data": get_processes_data(),
    }


@router.get("/ports")
def get_ports(current_user: dict = Depends(require_technician)):
    try:
        data = get_ports_data()

    except psutil.AccessDenied:
        return {
            "success": False,
            "message": "Access denied. Try running the server as administrator.",
            "timestamp": datetime.now(),
            "data": [],
        }

    return {
        "success": True,
        "message": "Ports information retrieved successfully",
        "timestamp": datetime.now(),
        "data": data,
    }


@router.get("/services")
def get_services(current_user: dict = Depends(require_technician)):
    services = get_services_data()

    if services == []:
        return {
            "success": False,
            "message": "Windows services are not supported on this system or no services were found.",
            "timestamp": datetime.now(),
            "data": [],
        }

    return {
        "success": True,
        "message": "Services retrieved successfully",
        "timestamp": datetime.now(),
        "data": services,
    }


@router.post("/processes/{pid}/kill")
def kill_process(pid: int, current_user: dict = Depends(require_admin)):
    try:
        result = kill_process_by_pid(pid)

        return {
            "success": True,
            "message": f"Process {pid} terminated successfully",
            "timestamp": datetime.now(),
            "data": result,
        }

    except psutil.NoSuchProcess:
        raise HTTPException(status_code=404, detail="Process not found")

    except psutil.AccessDenied:
        raise HTTPException(status_code=403, detail="Access denied")