from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.chat import router as chat_router

app = FastAPI()

app.include_router(health_router)
app.include_router(chat_router)