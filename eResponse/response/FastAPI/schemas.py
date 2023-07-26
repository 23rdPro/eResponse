from typing import List
from djantic import ModelSchema
from eResponse.response.models import File, Brief, Emergency
from eResponse.user.FastAPI.schemas import UserSchema, GroupSchema


class FileSchema(ModelSchema):
    file: str

    class Config:
        model = File
        include = ["id", "file"]


class BriefSchema(ModelSchema):
    files: List[FileSchema]
    # reporter: UserSchema

    class Config:
        model = Brief
        include = ["id", "title", "text", "files"]


class EmergencySchema(ModelSchema):
    emergency_type: GroupSchema
    respondents: List[UserSchema]
    briefs: List[BriefSchema]
    severity: int

    class Config:
        model = Emergency
        include = ["id", "emergency_type", "respondents", "briefs", "severity"]
