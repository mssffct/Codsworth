from litestar import Controller, Request, get

from .instances import Event
from config import get_logger

logger = get_logger("eventsLog")


class EventsController(Controller):
    path = "/events"

    @get("/")
    async def list_events(self, request: Request) -> Event:
        return Event(id=1, name="test_event")
