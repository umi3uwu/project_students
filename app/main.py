from fastapi import FastAPI

from app.controllers.student import router

app = FastAPI(title="Students Service")
app.include_router(router)