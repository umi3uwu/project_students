from fastapi import FastAPI

from app.controllers.student import router
from app.models.student import initialize_database


initialize_database()

app = FastAPI(title="Students Service")
app.include_router(router)