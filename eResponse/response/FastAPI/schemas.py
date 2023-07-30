from __future__ import annotations

from enum import Enum, IntEnum
from typing import List, Optional
from djantic import ModelSchema
from pydantic.main import BaseModel
from pydantic import FilePath
from eResponse.response.models import File, Brief, Emergency
from eResponse.user.FastAPI.schemas import UserSchema, GroupSchema


class FileSchema(ModelSchema):
    file: str

    class Config:
        model = File
        include = ["id", str("file")]


class BriefSchema(ModelSchema):
    title: str
    text: str
    # files: List[FileSchema]

    class Config:
        model = Brief
        include = ["title", "text", ]  # files


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
    # TERRIBLE: SeverityEnum = SeverityEnum.TERRIBLE
    # CATACLYSMIC: SeverityEnum = SeverityEnum.CATACLYSMIC


class GroupPydanticSchema(BaseModel):
    synthetic: GroupPydanticEnum = GroupPydanticEnum.synthetic
    natural: GroupPydanticEnum = GroupPydanticEnum.natural


class BriefPydanticSchema(BaseModel):
    title: str
    text: str
    files: List[bytes]


class CreateEmergencyPydanticSchema(BaseModel):
    emergency_type: str
    severity: int = 1
    brief_title: str
    brief_text: str
    files: List[bytes]

    # emergency_type: GroupPydanticSchema
    # severity: SeveritySchema
    # brief: BriefPydanticSchema


