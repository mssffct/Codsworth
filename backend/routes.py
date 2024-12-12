from events.routes import routes as event_routes
from notes.routes import routes as note_routes
from vault.routes import rotes as vault_routes

from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

routes = [
    Mount('/event', routes=event_routes),
    Mount('/note', routes=note_routes),
    Mount('/vault', routes=vault_routes),
    Mount('/static', app=StaticFiles(directory='statics'), name='static')
]