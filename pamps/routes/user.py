from typing import List

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select

from pamps.db import ActiveSession
from pamps.models.user import User, Social, UserRequest, UserResponse, SocialRequest
from pamps.auth import AuthenticatedUser
from pamps.models.post import Post, PostResponseWithReplies

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
async def list_users(*, session: Session = ActiveSession):
    """List all users"""
    users = session.exec(select(User)).all()
    return users


@router.get("/{username}/", response_model=UserResponse)
async def get_user_by_username(
    *, 
    session: Session = ActiveSession,
    username: str,
    include_following: bool = False
    ):
    """Get user by username"""

    filters = [User.username == username]
    if not include_following:
        filters.append(User.following == None)
    query = select(User).where(*filters)
    user = session.exec(query).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(*, session: Session = ActiveSession, user: UserRequest):
    """Creates new user"""
    db_user = User.from_orm(user)   # transform UserRequest in User
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.post("/follow/{id}", status_code=201)
async def follow_user(
    *, 
    session: Session = ActiveSession,
    current_user: User = AuthenticatedUser,
    user: SocialRequest,
):
    """Follows a user"""

    # checks if the user passed exists in the db
    user_query = session.exec(select(User).where(User.id == user.to_user_id)).first()
    if not user_query:
        raise HTTPException(status_code=404, detail="User not found")

    # Checks if the user is already being followed
    query = select(User).where(User.id == current_user.id)
    current = session.exec(query).first()
    current_following = current.following
    for follow in current_following:
        if user.to_user_id == follow.to_user_id:
            raise HTTPException(status_code=400, detail="User already followed")
    
  
    user.from_user_id = current_user.id
    follow_db = Social.from_orm(user)

    try:
        session.add(follow_db)
        session.commit()
        session.refresh(follow_db)
        return {"message": "User followed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/timeline", response_model=List[PostResponseWithReplies])
async def timeline(
    *,
    session: Session = ActiveSession,
    current_user: User = AuthenticatedUser,

):
    """Get all posts from user following"""
    # TODO: Tratar erro caso usuário não tenha seguido ninguem

    user = session.exec(select(User).where(User.id == current_user.id)).first()
    following = user.following
    to_user = [follow.to_user_id for follow in following]
    posts = session.exec(select(Post).join(User).where(
        User.id.in_(to_user),
        Post.parent == None
        )
    ).all()
    return posts
