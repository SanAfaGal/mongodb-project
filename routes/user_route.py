from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException

from config.db import db_conn
from models.user_model import User, UserCreate
from schemas.user_schema import user_entity, users_entity

name_router = 'users'
user_router = APIRouter(prefix=f'/{name_router}', tags=[name_router])
cursor = db_conn.get_collection(name_router)


@user_router.get('/', response_model=List[User])
def get_users(skip: int = 0, limit: int = 10):
    users = cursor.find().skip(skip).limit(limit)
    return users_entity(users)


@user_router.get('/{user_id}', response_model=User)
def get_user_by_id(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    user = cursor.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_entity(user)


@user_router.post('/', response_model=dict)
def add_user(new_user: UserCreate):
    result = cursor.insert_one(new_user.dict())
    document_id = result.inserted_id
    return {"_id created": str(document_id)}


@user_router.delete('/{user_id}', response_model=dict)
def delete_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = cursor.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")


@user_router.put('/{user_id}', response_model=dict)
def update_user(user_id: str, updated_user: UserCreate):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = cursor.replace_one({"_id": ObjectId(user_id)}, updated_user.dict())
    if result.modified_count == 1:
        return {"message": "User updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
