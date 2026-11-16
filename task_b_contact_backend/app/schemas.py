from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

MethodType = Literal["phone", "email", "social", "address"]

class ContactMethodIn(BaseModel):
    type: MethodType
    value: str = Field(min_length=1, max_length=500)
    label: str = Field(default="", max_length=100)

class ContactCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    notes: str = Field(default="", max_length=5000)
    is_favorite: bool = False
    methods: list[ContactMethodIn] = Field(default_factory=list)

class ContactUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    notes: str | None = Field(default=None, max_length=5000)
    is_favorite: bool | None = None
    methods: list[ContactMethodIn] | None = None

class ContactMethodOut(BaseModel):
    id: int
    type: MethodType
    value: str
    label: str

class ContactOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    notes: str
    is_favorite: bool
    methods: list[ContactMethodOut]
    created_at: str
    updated_at: str
