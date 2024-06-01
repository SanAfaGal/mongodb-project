from fastapi import FastAPI

from routes.comment_route import comment_router
from routes.event_route import event_router
from routes.user_route import user_router

app = FastAPI(
    title="PCJIC - Event Management API",
    description="The API for event management at Politécnico Colombiano JIC allows for the registration and "
                "management of events, talks, conferences, and meetings, storing data in a NoSQL database. "
                "The API handles detailed information for each event, including title, description, categories, "
                "date, location, attendees, speakers, organizing faculties, and comments. Additionally, it manages "
                "data for locations, cities, and users related to the events, facilitating searches and the display "
                "of organizers, facilitators, and attendees associated with each event."
)

app.include_router(user_router)
app.include_router(event_router)
app.include_router(comment_router)


@app.get('/')
def root():
    return {"message": "Go to http://127.0.0.1:8000/docs"}
