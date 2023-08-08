from __future__ import annotations

import aiofiles
from datetime import timedelta

from asgiref.sync import sync_to_async
from typing import Annotated, Optional

from jose import JWTError

from fastapi import HTTPException, Depends, File, status, UploadFile
from fastapi.security import OAuth2PasswordRequestForm

from starlette.responses import RedirectResponse

from eResponse.auth_token.FastAPI import schema as auth_token_schema
from eResponse.user.models import User

from eResponse.user.FastAPI.schemas import (
    UserSchema,
    GroupSchema,
    UserRegistrationSchema,
    CertificationSchema,
    UpdateUserSchema,
)
from eResponse import (
    oauth2_scheme,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    LOGIN_ACCESS_TOKEN_EXPIRE_MINUTES,
    PREFIX
)
from eResponse.api_helpers import to_schema

from .utils import (
    create_access_token_sync, create_user_sync, get_user_from_token,
    authenticate_user, get_all_users,
    filter_user_by_id, jwt_decode, get_user_from_payload,
    get_user_sync, create_group, create_certificate,

)


async def create_user(*, new_user: UserRegistrationSchema = Depends()):
    user = await create_user_sync(**new_user.dict())
    token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = await create_access_token_sync(
        {"sub": user.email}, expires_delta=token_expires)
    if user is not None:
        return RedirectResponse(
            url=f"{PREFIX}/users/{access_token}/activate")

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Incorrect email or password")


async def activate_user(token: Optional[str]):
    if token and isinstance(token, str):
        payload = await jwt_decode(token)
        user = await get_user_from_payload(payload)
        return {"is_activated": user.is_active}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="token not found")


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)]):
    http_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = await jwt_decode(token)
        email: str = payload.get("sub")
        user = await get_user_from_token(email)
        if email is None or user is None:
            raise http_exception

    except JWTError:
        raise http_exception
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.is_active:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Inactive User")


# async def logout(current_user: Depends(get_current_active_user)):  # TODO
#     pass


async def login(
        form: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    http_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    _user_check = await get_user_sync(email=form.username)
    if _user_check and not _user_check.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user")

    _user_authenticate = await authenticate_user(
        form.username, form.password)

    if _user_authenticate is None:
        raise http_exception

    token_expires = timedelta(minutes=int(LOGIN_ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = await create_access_token_sync(
        {"sub": _user_authenticate.email},
        expires_delta=token_expires)

    token_data = {
        "access_token": access_token,
        "user_id": str(_user_authenticate.id)
    }

    token_data.setdefault("token_type", "bearer")
    response_model = auth_token_schema.TokenModel(**token_data)

    return response_model


async def read_users_me(
        current_user: Annotated[UserSchema, Depends(get_current_active_user)]
):

    return await to_schema(current_user, UserSchema)


async def read_users():
    users = await get_all_users()
    return await to_schema(users, UserSchema)


async def get_user(user_id: str):
    user = await filter_user_by_id(user_id)
    if user is not None:
        return await to_schema(user, UserSchema)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="user not found")


CurrentUser = Depends(get_current_user)


async def update_user(
        curr: Annotated[User, CurrentUser],
        user: UpdateUserSchema = Depends(),
):
    curr_user = await User.filters.afilter(id=curr.id)
    data = user.dict(exclude_unset=True)
    data = {k: v for k, v in data.items() if v is not None}

    await curr_user.aupdate(**data)
    return await to_schema(curr_user, UserSchema)


async def update_user_group(
        user: Annotated[User, CurrentUser],
        group: GroupSchema = Depends()
):
    curr = await User.filters.afilter(id=user.id)
    created_group = await create_group(group.dict().get("name"))

    temp = await curr.aget()

    await sync_to_async(lambda: temp.groups.add(created_group))()

    return await to_schema(temp, UserSchema)


async def update_user_certification(
        user: Annotated[User, CurrentUser],
        certification: CertificationSchema = Depends(),
        file: UploadFile = File(...)
):
    curr = await User.filters.afilter(id=user.id)
    with aiofiles.open(
            f"eResponse/media/certificates/{file.filename}",
            "wb") as FILE:

        content = await file.read()
        await FILE.write(content)

    cert = await create_certificate(certification.dict())
    temp = await curr.aget()

    await sync_to_async(lambda: temp.certifications.add(cert))()


async def delete_user(*, user_id: str):
    user = await filter_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found")

    # assert hasattr(user, 'delete')  test
    await sync_to_async(lambda: user.delete())()
    return {"ok": True}
