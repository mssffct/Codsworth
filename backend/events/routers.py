from litestar import Router

from .controllers import EventsController

events_router = Router(path="/", route_handlers=[EventsController])
