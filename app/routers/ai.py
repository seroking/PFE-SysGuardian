from fastapi import APIRouter
from app.schemas.ia import AI_request
from app.services.system_service import get_cpu_data, get_memory_data, get_storage_data, get_summary_data,get_processes_data, get_ports_data, get_services_data
router = APIRouter(prefix="/ai", tags=["Ai"])

@router.post("/ask")
def ask_ai(request : AI_request):
  
  word_list = request.prompt.lower().split()



  key_words = {
    "cpu": [
        "cpu",
        "processor",
        "processors",
        "cpu usage"
    ],

    "memory": [
        "memory",
        "ram",
        "available memory"
    ],

    "storage": [
        "storage",
        "disk",
        "disks",
        "space"
    ],

    "summary": [
        "summary",
        "status",
        "overview"
    ],

    "processes": [
        "process",
        "processes",
        "tasks"
    ],

    "ports": [
        "port",
        "ports",
        "connections"
    ],

    "services": [
        "service",
        "services"
    ]
}
  
  functions_map = {
     "cpu": get_cpu_data,
     "memory": get_memory_data,
     "storage": get_storage_data,
     "summary": get_summary_data,
     "processes": get_processes_data,
     "ports": get_ports_data,
     "services": get_services_data
  }

  for intent, keywords in key_words.items():
    for keyword in keywords:
      if keyword in word_list:
          return functions_map[intent]()
  return {
    "success": False,
    "message": "Command not recognized"
}