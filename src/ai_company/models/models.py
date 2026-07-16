"""
Domain models for the AI Company Builder.

These models define every object that can exist in the company.
"""

from ai_company.models.models import Executive
from typing import List, Optional
from pydantic import BaseModel, Field


class Capability(BaseModel):
    """
    A capability that an agent possesses.
    """

    name: str
    description: str


class Permission(BaseModel):
    """
    OpenCode permissions.
    """

    read: bool = True
    write: bool = False
    edit: bool = False
    bash: bool = False
    task: bool = True


class Executive(BaseModel):

    id: str

    title: str

    department: str

    reports_to: str

    role: str

    mission: str

    responsibilities: List[str] = Field(default_factory=list)

    capabilities: List[Capability] = Field(default_factory=list)

    permissions: Permission = Field(default_factory=Permission)


class Specialist(BaseModel):

    id: str

    title: str

    department: str

    reports_to: str

    specialization: str

    responsibilities: List[str] = Field(default_factory=list)

    capabilities: List[Capability] = Field(default_factory=list)

    permissions: Permission = Field(default_factory=Permission)


class Department(BaseModel):

    id: str

    name: str

    executive: str

    purpose: str


class BoardAdvisor(BaseModel):

    id: str

    title: str

    inspirations: List[str]

    mission: str

    voting: bool = False


class Company(BaseModel):

    executives: List[Executive] = Field(default_factory=list)

    specialists: List[Specialist] = Field(default_factory=list)

    departments: List[Department] = Field(default_factory=list)

    board: List[BoardAdvisor] = Field(default_factory=list)