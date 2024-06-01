def comment_entity(item) -> dict:
    return {
        "_id": str(item.get("_id")),
        "text": item.get("text"),
        "user_id": str(item.get("user_id")),
        "event_id": str(item.get("event_id"))
    }


def comments_entity(entity) -> list:
    return [comment_entity(item) for item in entity]
