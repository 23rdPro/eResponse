from __future__ import annotations

from djantic.main import ModelSchema
from pydantic.main import BaseModel
from pydantic.dataclasses import dataclass
from eResponse.auth_token import models
# from pydantic.validators import

from eResponse.user.FastAPI.schemas import UserSchema


class TokenSchema(ModelSchema):
    user: UserSchema
    token_type: str or None = None

    class Config:
        model = models.Token
        include = ["token_type", "access_token", "user"]


@dataclass
class TokenModel(BaseModel):
    """
    pydantic, not djantic for token schema to avoid storing jwt in the db
    """
    token_type: str = "bearer"
    access_token: str
    user_id: str

    class Config:
        validate_assignment = True

    # @