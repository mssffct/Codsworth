import logging

from litestar import Controller, Request, get

from .instances import Event


logger = logging.getLogger('eventsLog')

class EventsController(Controller):
    path = '/events'

    @get('/')
    async def list_events(self, request: Request) -> Event:
        logger.debug('hello from events')
        return Event(id=1, name="test_event")
