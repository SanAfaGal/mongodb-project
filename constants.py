from bson import ObjectId


def CONVERT_TO_OBJECT_IDS(item: dict, *keys: str) -> dict:
    """
    Convert specified keys in the dictionary to ObjectId.

    Args:
        item (dict): Dictionary containing the items.
        keys (str): Keys to be converted to ObjectId.

    Returns:
        dict: Dictionary with specified keys converted to ObjectId.
    """
    for key in keys:
        if key in item:
            item[key] = [ObjectId(value) for value in item[key]]
    return item
