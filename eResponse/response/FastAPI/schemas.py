from typing import List
from djantic import ModelSchema
from eResponse.response.models import Picture, Video, Brief, Emergency
from eResponse.user.FastAPI.schemas import UserSchema, GroupSchema


class PictureSchema(ModelSchema):
    class Config:
        model = Picture
        include = ["__annotations__"]


class VideoSchema(ModelSchema):
    class Config:
        model = Video


class BriefSchema(ModelSchema):
    picture: List[PictureSchema] = List[PictureSchema]
    videos: List[VideoSchema] = List[VideoSchema]

    class Config:
        model = Brief


class EmergencySchema(ModelSchema):
    type: List[GroupSchema]
    respondents: List[UserSchema]

    class Config:
        model = Emergency
