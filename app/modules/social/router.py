
# =======================
# File: app/modules/social/router.py
# Path: app/modules/social/router.py
# =======================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import Post, User, Doctor, Pharmacy
from pydantic import BaseModel
from typing import List, Optional

social_router = APIRouter()

class PostCreate(BaseModel):
    title: str
    content: str
    post_type: str  # health_tip, combo_plan, general
    image_url: Optional[str] = None

@social_router.get("/posts")
async def get_posts(
    post_type: Optional[str] = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    query = db.query(Post).join(User)
    
    if post_type:
        query = query.filter(Post.post_type == post_type)
    
    posts = query.order_by(Post.created_at.desc()).limit(limit).all()
    
    # Add author information
    posts_with_authors = []
    for post in posts:
        post_dict = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "post_type": post.post_type,
            "image_url": post.image_url,
            "likes": post.likes,
            "created_at": post.created_at,
            "author": {
                "user_type": post.user.user_type,
                "name": "Unknown"
            }
        }
        
        # Get author name based on user type
        if post.user.user_type == "doctor" and post.user.doctor:
            post_dict["author"]["name"] = post.user.doctor.name
        elif post.user.user_type == "pharmacy" and post.user.pharmacy:
            post_dict["author"]["name"] = post.user.pharmacy.name
        
        posts_with_authors.append(post_dict)
    
    return posts_with_authors

@social_router.post("/posts")
async def create_post(
    user_id: int,
    post_data: PostCreate,
    db: Session = Depends(get_db)
):
    post = Post(
        user_id=user_id,
        title=post_data.title,
        content=post_data.content,
        post_type=post_data.post_type,
        image_url=post_data.image_url
    )
    
    db.add(post)
    db.commit()
    db.refresh(post)
    
    return post

@social_router.put("/posts/{post_id}/like")
async def like_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post.likes += 1
    db.commit()
    
    return {"message": "Post liked", "likes": post.likes}
