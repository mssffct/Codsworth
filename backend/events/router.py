from litestar import Router

from .views import list_events

events_router = Router(path="/events", route_handlers=[list_events])
