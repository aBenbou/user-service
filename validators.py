from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List
from datetime import datetime

class UserProfileBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileUpdate(BaseModel):
    username: Optional[constr(min_length=3, max_length=50)] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None

class UserProfileResponse(UserProfileBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserProfileList(BaseModel):
    users: List[UserProfileResponse]
    total: int
    page: int
    per_page: int 