from typing import List, Type, Callable, Any

from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from config.db import db_conn


def create_router(
        name_router: str,
        document_model: Type[BaseModel],
        document_create_model: Type[BaseModel],
        entity: Callable[[Any], dict],
        entity_list: Callable[[Any], List[dict]]
):
    router = APIRouter(prefix=f'/{name_router}', tags=[name_router])
    collection = db_conn.get_collection(name_router)

    @router.get('/', response_model=List[document_model], name=f"Get {name_router}")
    def get_documents(skip: int = 0, limit: int = 10):
        documents = collection.find().skip(skip).limit(limit)
        return entity_list(documents)

    @router.get('/{document_id}', response_model=document_model, name=f"Get {name_router[:-1]} By Id")
    def get_document_by_id(document_id: str):
        if not ObjectId.is_valid(document_id):
            raise HTTPException(status_code=400, detail="Invalid ID format")
        document = collection.find_one({"_id": ObjectId(document_id)})
        if document is None:
            raise HTTPException(status_code=404, detail=f"{name_router[:-1]} not found")
        return entity(document)

    @router.post('/', response_model=dict, name=f"Add {name_router[:-1]}")
    def create_document(new_document: document_create_model):
        result = collection.insert_one(new_document.dict())
        document_id = result.inserted_id
        return {"_id created": str(document_id)}

    @router.delete('/{document_id}', response_model=dict, name=f"Delete {name_router[:-1]}")
    def delete_document(document_id: str):
        if not ObjectId.is_valid(document_id):
            raise HTTPException(status_code=400, detail="Invalid ID format")
        result = collection.delete_one({"_id": ObjectId(document_id)})
        if result.deleted_count == 1:
            return {"message": f"{name_router} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"{name_router} not found")

    @router.put('/{document_id}', response_model=dict, name=f"Update {name_router[:-1]}")
    def update_document(document_id: str, updated_document: document_create_model):
        if not ObjectId.is_valid(document_id):
            raise HTTPException(status_code=400, detail="Invalid ID format")
        result = collection.replace_one({"_id": ObjectId(document_id)}, updated_document.dict())
        if result.modified_count == 1:
            return {"message": f"{name_router} updated successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"{name_router} not found")

    return router
