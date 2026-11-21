
from typing import Optional
from pydantic import BaseModel, Field


class Project(BaseModel):
    name: Optional[str] = None
    description: str


class Education(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    graduation_year: Optional[str] = None


class ResumeInformation(BaseModel):
    candidate_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    total_experience_years: Optional[float] = None

    skills: list[str] = Field(default_factory=list)

    education: list[Education] = Field(default_factory=list)

    projects: list[Project] = Field(default_factory=list)

from typing import Optional
from pydantic import BaseModel, Field


class Project(BaseModel):
    name: Optional[str] = None
    description: str


class Education(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    graduation_year: Optional[str] = None


class ResumeInformation(BaseModel):
    candidate_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    total_experience_years: Optional[float] = None

    skills: list[str] = Field(default_factory=list)

    education: list[Education] = Field(default_factory=list)

    projects: list[Project] = Field(default_factory=list)
