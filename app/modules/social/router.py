# =======================
# File: app/modules/social/router.py
# Path: app/modules/social/router.py
# =======================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from database.connection import get_db
from database.models import Post, User
from pydantic import BaseModel
from modules.auth.dependencies import get_current_user # CORRECTED: Import security dependency

social_router = APIRouter()

class PostCreate(BaseModel):
    title: str
    content: str
    post_type: str  # health_tip, combo_plan, general
    image_url: Optional[str] = None

class Author(BaseModel):
    user_type: str
    name: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    post_type: str
    image_url: Optional[str] = None
    likes: int
    created_at: str
    author: Author

    class Config:
        from_attributes = True


@social_router.get("/posts", response_model=List[PostResponse])
async def get_posts(
    post_type: Optional[str] = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Fetches a list of posts. This is a public endpoint and does not require authentication.
    """
    query = db.query(Post).join(User).order_by(Post.created_at.desc())
    
    if post_type:
        query = query.filter(Post.post_type == post_type)
    
    posts = query.limit(limit).all()
    
    # Add author information to each post
    posts_with_authors = []
    for post in posts:
        author_name = "Unknown"
        if post.user.user_type == "doctor" and post.user.doctor:
            author_name = post.user.doctor.name
        elif post.user.user_type == "pharmacy" and post.user.pharmacy:
            author_name = post.user.pharmacy.name
        
        post_data = post.__dict__
        post_data['author'] = {"user_type": post.user.user_type, "name": author_name}
        posts_with_authors.append(post_data)
    
    return posts_with_authors

@social_router.post("/posts", response_model=PostResponse)
async def create_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # CORRECTED: Protected endpoint
):
    """
    Creates a new post. The author is the currently authenticated user.
    """
    # CORRECTED: User ID is now securely taken from the token, not a parameter
    post = Post(
        user_id=current_user.id,
        title=post_data.title,
        content=post_data.content,
        post_type=post_data.post_type,
        image_url=post_data.image_url
    )
    
    db.add(post)
    db.commit()
    db.refresh(post)
    
    # Manually construct the response to match the PostResponse model
    author_name = "Unknown"
    if current_user.user_type == "doctor" and current_user.doctor:
        author_name = current_user.doctor.name
    elif current_user.user_type == "pharmacy" and current_user.pharmacy:
        author_name = current_user.pharmacy.name
        
    response_data = post.__dict__
    response_data['author'] = {"user_type": current_user.user_type, "name": author_name}

    return response_data

@social_router.put("/posts/{post_id}/like")
async def like_post(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # CORRECTED: Protected endpoint
):
    """
    Likes a post. Requires user to be authenticated.
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # In a real app, you would add logic to prevent double-liking
    post.likes += 1
    db.commit()
    
    return {"message": "Post liked", "likes": post.likes}