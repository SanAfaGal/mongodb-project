from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException

from config.db import db_conn
from models.comment_model import Comment, CommentCreate
from schemas.comment_schema import comment_entity, comments_entity

name_router = 'comments'
comment_router = APIRouter(prefix=f'/{name_router}', tags=[name_router])
cursor = db_conn.get_collection(name_router)


@comment_router.get('/', response_model=List[Comment])
def get_comments(skip: int = 0, limit: int = 10):
    comments = cursor.find().skip(skip).limit(limit)
    return comments_entity(comments)


@comment_router.get('/{comment_id}', response_model=Comment)
def get_comment_by_id(comment_id: str):
    if not ObjectId.is_valid(comment_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    comment = cursor.find_one({"_id": ObjectId(comment_id)})
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment_entity(comment)


@comment_router.post('/', response_model=dict)
def add_comment(new_comment: CommentCreate):
    new_comment_dict = new_comment.dict()

    new_comment_dict.update({
        'user_id': ObjectId(new_comment_dict.pop('user_id')),
        'event_id': ObjectId(new_comment_dict.pop('event_id'))
    })

    result = cursor.insert_one(new_comment_dict)
    document_id = result.inserted_id
    return {"_id created": str(document_id)}


@comment_router.delete('/{comment_id}', response_model=dict)
def delete_comment(comment_id: str):
    if not ObjectId.is_valid(comment_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = cursor.delete_one({"_id": ObjectId(comment_id)})
    if result.deleted_count == 1:
        return {"message": "Comment deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Comment not found")


@comment_router.put('/{comment_id}', response_model=dict)
def update_comment(comment_id: str, updated_comment: CommentCreate):
    if not ObjectId.is_valid(comment_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = cursor.replace_one({"_id": ObjectId(comment_id)}, updated_comment.dict())
    if result.modified_count == 1:
        return {"message": "Comment updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Comment not found")
