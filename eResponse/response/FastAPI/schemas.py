from __future__ import annotations

import os
from enum import Enum, IntEnum
from typing import List
from djantic import ModelSchema
# from pydantic.main import BaseModel
from pydantic import BaseModel, FilePath
from eResponse.response.models import File, Brief, Emergency
from eResponse.user.FastAPI.schemas import UserSchema


# for file in os.listdir():

# class FileFieldPydantic(BaseModel):
#     file: FilePath = ""


class FileSchema(ModelSchema):
    # file: FileFieldPydantic

    class Config:
        model = File
        include = ["id", ]  # TODO
        arbitrary_types_allowed = True


class EmergencyBriefSchema(ModelSchema):
    files: List[FileSchema]

    class Config:
        model = Brief
        include = ["id", "title", "text", "files"]


class EmergencySchema(ModelSchema):
    respondents: List[UserSchema]
    briefs: List[EmergencyBriefSchema]

    class Config:
        model = Emergency
        include = [
            "id",
            "created_at",
            "updated_at",
            "respondents",
            "emergency_type",
            "briefs",
            "severity",
        ]


class GroupPydanticEnum(str, Enum):
    synthetic = "synthetic"
    natural = "natural"


class SeverityEnum(IntEnum):
    BAD = 1
    TERRIBLE = 2
    CATACLYSMIC = 3


class CreateEmergencyResponseSchema(ModelSchema):
    emergency_type: GroupPydanticEnum
    manager: str
    severity: SeverityEnum

    class Config:
        model = Emergency
        include = ["emergency_type", "severity"]


class SeveritySchema(BaseModel):
    BAD: SeverityEnum = SeverityEnum.BAD
    TERRIBLE: SeverityEnum = SeverityEnum.TERRIBLE
    CATACLYSMIC: SeverityEnum = SeverityEnum.CATACLYSMIC


class GroupPydanticSchema(BaseModel):
    synthetic: GroupPydanticEnum = GroupPydanticEnum.synthetic
    natural: GroupPydanticEnum = GroupPydanticEnum.natural


class BriefPydanticSchema(BaseModel):
    brief_title: str
    brief_text: str


class CreateEmergencyPydanticSchema(BaseModel):
    emergency_type: str
    severity: int = 1
    brief_title: str
    brief_text: str
    files: List[bytes]

    # emergency_type: GroupPydanticSchema
    # severity: SeveritySchema
    # brief: BriefPydanticSchema


