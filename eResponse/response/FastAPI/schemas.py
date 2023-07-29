from __future__ import annotations

from enum import Enum, IntEnum
from typing import List, Optional
from djantic import ModelSchema
from pydantic.main import BaseModel
from eResponse.response.models import File, Brief, Emergency
from eResponse.user.FastAPI.schemas import UserSchema, GroupSchema


class FileSchema(ModelSchema):
    file: str

    class Config:
        model = File
        include = ["id", "file"]


class BriefSchema(ModelSchema):
    files: Optional[List[FileSchema]]
    # reporter: UserSchema

    class Config:
        model = Brief
        include = ["title", "text"]


class EmergencySchema(ModelSchema):
    emergency_type: GroupSchema
    respondents: Optional[List[UserSchema]]
    briefs:  Optional[List[BriefSchema]]
    severity: int = 1

    class Config:
        model = Emergency
        include = ["emergency_type", "briefs", "severity",]


class GroupPydanticEnum(str, Enum):
    synthetic = "synthetic"
    natural = "natural"


class CreateEmergencyResponseSchema(ModelSchema):
    emergency_type: GroupSchema

    class Config:
        model = Emergency
        include = ["emergency_type"]


class SeverityEnum(IntEnum):
    BAD = 1
    TERRIBLE = 2
    CATACLYSMIC = 3


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


