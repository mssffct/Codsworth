from litestar import Router

from .controllers import NotesController


notes_router = Router(path="/", route_handlers=[NotesController])
