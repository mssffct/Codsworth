from litestar import Controller, Request, get

from .instances import Event


class EventsController(Controller):
    path = '/events'

    @get('/')
    async def list_events(self, request: Request) -> Event:
        return Event(id=1, name="test_event")
