def user_entity(item) -> dict:
    return {
        "_id": str(item["_id"]),
        "username": item["username"],
        "full_name": item["full_name"],
        "relationship": item["relationship"],
        "email": item["email"],
        "city": {
            "name": item["city"]["name"],
            "department": item["city"]["department"],
            "country": item["city"]["country"]
        }
    }


def users_entity(entity) -> list:
    return [user_entity(item) for item in entity]
