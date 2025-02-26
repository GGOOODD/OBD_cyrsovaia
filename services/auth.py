from fastapi import HTTPException, status, Response, Request
from fastapi.responses import JSONResponse
from database import new_session, UserModel
from schemas import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
import jwt


class Auth:
    key = "RSGSDFGEFA3W5Y"
    algorithm = "HS256"
    @classmethod
    async def register(cls, data: RegInfo):
        if data.password != data.repeat_password:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "Пароли не совпадают"
            )

        user_field = UserModel(
            name=data.name,
            surname=data.surname,
            patronymic=data.patronymic,
            email=data.email,
            password=jwt.encode({"password": data.password}, Auth.key, Auth.algorithm),
            admin=False
        )
        async with new_session() as session:
            session.add(user_field)
            try:
                await session.flush()
            except IntegrityError:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    "Данная почта уже зарегистрирована"
                )
            await session.commit()

            response = JSONResponse(GetUser(**user_field.__dict__).model_dump(), 200)
            response.set_cookie(
                key="token",
                value=jwt.encode({"id": user_field.id}, Auth.key, Auth.algorithm)
            )
            return response

    @classmethod
    async def login(cls, data: LogInfo):
        query = select(UserModel).filter_by(
            email=data.email, password=jwt.encode({"password": data.password}, Auth.key, Auth.algorithm)
        )
        async with new_session() as session:
            result = await session.execute(query)
        user = result.scalars().first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Неверная почта/пароль",
            )

        response = JSONResponse(GetUser(**user.__dict__).model_dump(), 200)
        response.set_cookie(
            key="token",
            value=jwt.encode({"id": user.id}, Auth.key, Auth.algorithm)
        )
        return response

    @classmethod
    async def logout(cls, request: Request, response: Response):
        token = request.cookies.get("token")
        if token is None:
            return JSONResponse(Inform(detail="You already logged out", field_id=None).model_dump(), 200)
        response = JSONResponse(Inform(detail="Logged out", field_id=None).model_dump(), 200)
        response.delete_cookie("token")
        return response
