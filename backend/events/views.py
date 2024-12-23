from litestar import Request, get

from .instances import Event


@get('/')
async def list_events(request: Request) -> Event:
    return Event(id=1, name="test_event")
