from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from src.models.conta_model import Conta
from src.schemas.auth_schemas import Token
from src.auth_utils import get_current_user
from src.services.auth_service import AuthService  # Importamos o serviço

rota = APIRouter(tags=['auth'])

# Injeção de dependência para o Service
async def get_auth_service(session: Annotated[AsyncSession, Depends(get_db)]):
    return AuthService(session)

AuthServ = Annotated[AuthService, Depends(get_auth_service)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
CurrentUser = Annotated[Conta, Depends(get_current_user)]


@rota.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2Form, auth_service: AuthServ):
    # O Controller apenas delega a tarefa
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    return auth_service.generate_token_data(user.email)


@rota.post('/refresh_token', response_model=Token)
async def refresh_access_token(user: CurrentUser, auth_service: AuthServ):
    # Reaproveitamos a lógica de geração de token
    return auth_service.generate_token_data(user.email)