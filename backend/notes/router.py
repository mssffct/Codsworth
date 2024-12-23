from litestar import Router

from .views import list_notes


notes_router = Router(path="/notes", route_handlers=[list_notes])
