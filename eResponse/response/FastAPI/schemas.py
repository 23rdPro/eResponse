from typing import List
from djantic import ModelSchema
from eResponse.response.models import Picture, Video, Brief, Emergency
from eResponse.user.FastAPI.schemas import UserSchema, GroupSchema


class PictureSchema(ModelSchema):
    class Config:
        model = Picture
        include = "__annotations__"


class VideoSchema(ModelSchema):
    class Config:
        model = Video
        include = "__annotations__"


class BriefSchema(ModelSchema):
    pictures: List[PictureSchema]
    videos: List[VideoSchema]
    reporter: UserSchema

    class Config:
        model = Brief
        include = ["reporter", "title", "text", "pictures", "videos"]


class EmergencySchema(ModelSchema):
    emergency_type: GroupSchema
    respondents: List[UserSchema]
    briefs: List[BriefSchema]

    class Config:
        model = Emergency
        include = ["emergency_type", "respondents", "briefs", "severity"]
