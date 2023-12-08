"""Post related data models"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional, List

from pydantic import BaseModel, Extra
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from pamps.models.user import User


class Post(SQLModel, table=True):
    """Represents the Post Model"""

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    date: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user_id: Optional[int] = Field(foreign_key="user.id")
    parent_id: Optional[int] = Field(foreign_key="post.id")

    # It populates a `.posts` attribute to the `User` model.
    user: Optional["User"] = Relationship(back_populates="posts")

    # It populates `.replies` on this model
    parent: Optional["Post"] = Relationship(
        back_populates="replies",
        sa_relationship_kwargs=dict(remote_side="Post.id"),
    )
    # This lists all children to this post
    replies: List["Post"] = Relationship(back_populates="parent")

    post_likes: List["Like"] = Relationship(back_populates="posts")

    def __lt__(self, other):
        """This enables post.replies.sort() to sort by date"""
        return self.date < other.date


class PostResponse(BaseModel):
    """Serializer for Post Response"""

    id: int
    text: str
    date: datetime
    user_id: int
    parent_id: Optional[int]


class PostResponseWithReplies(PostResponse):
    """Serializer for Post response with replies"""
    
    replies: Optional[List["PostResponse"]] = None

    class Config:
        orm_mode = True


class PostRequest(BaseModel):
    """Serializer for Post request payload"""

    parent_id: Optional[int]
    text: str

    class Config:
        extra = Extra.allow
        arbitrary_types_allowed = True


class Like(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user: Optional[int] = Field(foreign_key="user.id", nullable=False)
    post: Optional[int] = Field(foreign_key="post.id", nullable=False)

    # It populates a `.post_likes` attribute to the `Post` model
    posts: List["Post"] = Relationship(back_populates="post_likes")

    # It populates a `.user_likes` attribute to the `User` model
    users: List["User"] = Relationship(back_populates="user_likes")


class LikeResponse(BaseModel):
    """Serializer for Like response"""

    id: int
    post: int
    user: int
    

class LikeRequest(BaseModel):
    """Serializer for Like request payload"""

    post: int

    class Config:
        extra = Extra.allow
        arbitrary_types_allowed = True
