from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.conta_model import Conta
from src.auth_utils import verify_password, create_access_token

class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def authenticate_user(self, email: str, password: str) -> Conta:
        user = await self.session.scalar(
            select(Conta).where(Conta.email == email)
        )

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Incorrect email or password',
            )
        
        return user

    def generate_token_data(self, email: str) -> dict:
        access_token = create_access_token(data={'sub': email})
        return {'access_token': access_token, 'token_type': 'bearer'}   
