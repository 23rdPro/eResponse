from typing import List
from djantic import ModelSchema
from eResponse.response.models import Emergency, Brief, Picture, Video
from eResponse.user.FastAPI.schema import UserSchema, GroupSchema


class PictureSchema(ModelSchema):
    class Config:
        model = Picture


class VideoSchema(ModelSchema):
    class Config:
        model = Video


class BriefSchema(ModelSchema):
    picture = List[PictureSchema]
    videos = List[VideoSchema]

    class Config:
        model = Brief


class EmergencySchema(ModelSchema):
    type: List[GroupSchema]
    respondents: List[UserSchema]

    class Config:
        model = Emergency
