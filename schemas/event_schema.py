def event_entity(item) -> dict:
    location = item.get("location")
    city = location.get("city")
    return {
        "_id": str(item.get("_id")),
        "title": item.get("title"),
        "description": item.get("description"),
        "categories": item.get("categories"),
        "date": item.get("date"),
        "location": {
            "name": location.get("name"),
            "address": location.get("address"),
            "city": {
                "name": city.get("name"),
                "department": city.get("department"),
                "country": city.get("country")
            }
        },
        "organizers": item.get("organizers"),
        "attendees": item.get("attendees"),
        "speakers": item.get("speakers"),
        "comments": item.get("comments")
    }


def events_entity(entity) -> list:
    return [event_entity(item) for item in entity]
