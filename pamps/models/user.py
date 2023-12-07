from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from pamps.security import HashedPassword
from pydantic import BaseModel, Extra
from datetime import datetime

if TYPE_CHECKING:
    from pamps.models.post import Post

class User(SQLModel, table=True):
    """Represents the User Model"""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False)
    username: str = Field(unique=True, nullable=False)
    avatar: Optional[str] = None
    bio: Optional[str] = None
    password: HashedPassword

    posts: List["Post"] = Relationship(back_populates="user")

    followers: List["Social"] = Relationship(
        back_populates="to_user",
        sa_relationship_kwargs={"primaryjoin": 'User.id == Social.to_user_id'}
        )
    
    following: List["Social"] = Relationship(
        back_populates="from_user",
        sa_relationship_kwargs={
            "primaryjoin": 'User.id == Social.from_user_id'
        }
    )


class UserResponse(BaseModel):
    """Serializer for User Response"""

    username: str
    avatar: Optional[str] = None
    bio: Optional[str] = None
    

class UserRequest(BaseModel):
    """Serializer for User request payload"""

    email: str
    username: str
    password: str
    avatar: Optional[str] = None
    bio: Optional[str] = None


class Social(SQLModel, table=True):
    """Represents the Social Model"""

    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    from_user_id: Optional[int] = Field(foreign_key="user.id", nullable=False)
    to_user_id: int = Field(foreign_key="user.id", nullable=False)

    # It populates a `.following` attribute to the `User` model.
    to_user: Optional["User"] = Relationship(
        back_populates="following",
        sa_relationship_kwargs={"primaryjoin": 'Social.to_user_id == User.id'},
        )
    
    # It populates a `.followers` attribute to the `User` model.
    from_user: Optional["User"] = Relationship(
        back_populates="followers",
        sa_relationship_kwargs={
            "primaryjoin": 'Social.from_user_id == User.id'
        }
    )


class SocialResponse(BaseModel):
    """Serializer for Social response"""

    id: int
    date: datetime
    from_user_id: int
    to_user_id: int


class SocialRequest(BaseModel):
    """Serializer for Social request payload """
    
    to_user_id: int

    class Config:
        extra = Extra.allow
        arbitrary_types_allowed = True

