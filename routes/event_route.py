from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException

from config.db import db_conn
from models.event_model import EventCreate, EventShow
from pipelines import GET_EVENT_PIPELINE
from constants import CONVERT_TO_OBJECT_IDS
from schemas.event_schema import event_entity, events_entity

name_router = 'events'
event_router = APIRouter(prefix=f'/{name_router}', tags=[name_router])
cursor = db_conn.get_collection(name_router)


@event_router.get('/', response_model=List[EventShow])
def get_events(skip: int = 0, limit: int = 10):
    pipeline = GET_EVENT_PIPELINE(offset=skip, batch_size=limit)
    events = cursor.aggregate(pipeline)
    return events_entity(events)


@event_router.get('/{event_id}', response_model=EventShow)
def get_event_by_id(event_id: str):
    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    pipeline = GET_EVENT_PIPELINE(event_identifier=event_id)
    event = list(cursor.aggregate(pipeline))
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return event_entity(event[0])


@event_router.post('/', response_model=dict)
def add_event(new_event: EventCreate):
    new_event_dict = CONVERT_TO_OBJECT_IDS(new_event.dict(), "attendees", "speakers")
    result = cursor.insert_one(new_event_dict)
    document_id = result.inserted_id
    return {"_id created": str(document_id)}


@event_router.delete('/{event_id}', response_model=dict)
def delete_event(event_id: str):
    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = cursor.delete_one({"_id": ObjectId(event_id)})
    if result.deleted_count == 1:
        return {"message": "Event deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Event not found")


@event_router.put('/{event_id}', response_model=dict)
def update_event(event_id: str, updated_event: EventCreate):
    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    updated_event_dict = CONVERT_TO_OBJECT_IDS(updated_event.dict(), "attendees", "speakers")
    result = cursor.replace_one({"_id": ObjectId(event_id)}, updated_event_dict)

    if result.modified_count == 1:
        return {"message": "Event updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Event not found")
