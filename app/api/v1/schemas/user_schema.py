import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.domain.entities.user import UserRole, UserStatus


class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str
    full_name: str | None
    role: UserRole
    status: UserStatus
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserUpdateRequest(BaseModel):
    full_name: str | None = Field(default=None, max_length=120)
    username: str | None = Field(default=None, min_length=3, max_length=50)


class AdminUserUpdateRequest(UserUpdateRequest):
    role: UserRole | None = None
    status: UserStatus | None = None
    is_verified: bool | None = None
