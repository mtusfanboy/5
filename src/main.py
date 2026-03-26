from fastapi import FastAPI
from src.routers.user import router

app = FastAPI()
app.include_router(router)
