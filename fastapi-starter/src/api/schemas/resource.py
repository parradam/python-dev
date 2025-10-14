from pydantic import BaseModel, field_validator

MIN_NAME_LENGTH = 3


class ResourceBase(BaseModel):
    name: str
    link: str | None = None
    isbn: str | None = None

    @field_validator("name")
    @classmethod
    def name_min_length(cls, v: str) -> str:
        if len(v) < MIN_NAME_LENGTH:
            msg = f"name must be at least {MIN_NAME_LENGTH} characters"
            raise ValueError(msg)
        return v


class ResourceIn(ResourceBase):
    pass


class ResourceOut(ResourceBase):
    id: int


class ResourceUpdate(BaseModel):
    name: str | None = None
    link: str | None = None
    isbn: str | None = None

    @field_validator("name")
    @classmethod
    def name_min_length(cls, v: str) -> str:
        if len(v) < MIN_NAME_LENGTH:
            msg = f"name must be at least {MIN_NAME_LENGTH} characters"
            raise ValueError(msg)
        return v
