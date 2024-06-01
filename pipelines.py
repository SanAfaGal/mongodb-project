from bson import ObjectId


def GET_EVENT_PIPELINE(event_identifier: str = None, offset: int = 0, batch_size: int = 10):
    match_stage = {"$match": {}}
    if event_identifier:
        match_stage["$match"]["_id"] = ObjectId(event_identifier)

    pipeline = [
        match_stage,
        {
            '$lookup': {
                'from': 'users',
                'let': {
                    'attendee_ids': '$attendees',
                    'speaker_ids': '$speakers'
                },
                'pipeline': [
                    {
                        '$match': {
                            '$expr': {
                                '$or': [
                                    {
                                        '$in': [
                                            '$_id', '$$attendee_ids'
                                        ]
                                    }, {
                                        '$in': [
                                            '$_id', '$$speaker_ids'
                                        ]
                                    }
                                ]
                            }
                        }
                    }, {
                        '$project': {
                            '_id': 1,
                            'full_name': 1,
                            'relationship': 1,
                            'email': 1
                        }
                    }
                ],
                'as': 'users'
            }
        }, {
            '$lookup': {
                'from': 'comments',
                'localField': '_id',
                'foreignField': 'event_id',
                'as': 'comments'
            }
        }, {
            '$lookup': {
                'from': 'users',
                'localField': 'comments.user_id',
                'foreignField': '_id',
                'as': 'comment_users'
            }
        }, {
            '$addFields': {
                'attendees': {
                    '$filter': {
                        'input': '$users',
                        'as': 'user',
                        'cond': {
                            '$in': [
                                '$$user._id', '$attendees'
                            ]
                        }
                    }
                },
                'speakers': {
                    '$filter': {
                        'input': '$users',
                        'as': 'user',
                        'cond': {
                            '$in': [
                                '$$user._id', '$speakers'
                            ]
                        }
                    }
                },
                'comments': {
                    '$map': {
                        'input': '$comments',
                        'as': 'comment',
                        'in': {
                            'text': '$$comment.text',
                            'username': {
                                '$arrayElemAt': [
                                    '$comment_users.username', {
                                        '$indexOfArray': [
                                            '$comment_users._id', '$$comment.user_id'
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        }, {
            '$project': {
                '_id': 1,
                'title': 1,
                'description': 1,
                'categories': 1,
                'date': 1,
                'location': 1,
                'organizers': 1,
                'attendees': {
                    'full_name': 1,
                    'relationship': 1,
                    'email': 1
                },
                'speakers': {
                    'full_name': 1,
                    'relationship': 1,
                    'email': 1
                },
                'comments': 1
            }
        }
    ]

    if offset > 0:
        pipeline.append({"$skip": offset})

    if batch_size > 0:
        pipeline.append({"$limit": batch_size})

    return pipeline
