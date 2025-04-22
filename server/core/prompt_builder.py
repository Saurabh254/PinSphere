__all__ = ["PromptBuilder"]
from pydantic import BaseModel, Field, field_validator


class PromptBuilder(BaseModel):
    USER_PROMPT: str = Field(alias="user_prompt")
    VERSION: str = Field(alias="version")
    SYSTEM_PROMPT: str = Field(alias="system_prompt")

    @field_validator("VERSION")
    def validate_version(cls, version: str):
        if version.startswith("v"):
            return version
        raise ValueError("Invalid Prompt Version, version must start with 'v'")
