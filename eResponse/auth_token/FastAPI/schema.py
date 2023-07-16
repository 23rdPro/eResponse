from djantic.main import ModelSchema
from eResponse.auth_token import models


class TokenSchema(ModelSchema):

    class Config:
        model = models.Token
        include = ["token_type", "access_token", "user"]
