import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class UserLoginSchema(BaseModel):
    username: str = Field(..., max_length=250, description="Username of the User")
    password: str = Field(..., max_length=250, description="Password of the User")


class UserRegisterSchema(BaseModel):
    username: str = Field(..., max_length=250, description="Username of the User")
    password: str = Field(..., max_length=250, description="Password of the User")
    password_confirm: str = Field(..., max_length=250, description="Confirm Password of the User")

    @field_validator("password_confirm")
    def check_password_confirm_match(cls, password_confirm, validation):
        if password_confirm != validation.data.get('password'):
            raise ValueError("password doesn't match!")
        return password_confirm
