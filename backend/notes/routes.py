from starlette.routing import Route

from views import Note

routes = [
    Route('/', Note),
]
