from fastapi import FastAPI

from src.controllers import auth_controller, conta_controller, transacao_controller
from database import engine, Base
from src import models

app = FastAPI()

@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth_controller.rota, prefix='/auth')
app.include_router(conta_controller.rota, prefix='/conta')
app.include_router(transacao_controller.rota, prefix='/transacao')
