from starlette.routing import Route

from .views import Event

routes = [
    Route('/', Event),
]