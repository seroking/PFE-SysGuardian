from fastapi import FastAPI
from app.routers.system import router as system_router
from app.routers.auth import router as auth_router
from app.routers.ai import router as ai_router
from app.database import engine, Base
from app.routers.users import router as user_router
Base.metadata.create_all(bind=engine)
app = FastAPI(title="AI Sys")


@app.get('/')
def root():
    return {"message": "SysGuardian API is running"}


app.include_router(system_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(ai_router)