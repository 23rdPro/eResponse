from __future__ import annotations

from djantic.main import ModelSchema
from eResponse.auth_token import models

from eResponse.user.FastAPI.schemas import UserSchema


class TokenSchema(ModelSchema):
    user: UserSchema
    token_type: str or None = None

    class Config:
        model = models.Token
        include = ["token_type", "access_token", "user"]
