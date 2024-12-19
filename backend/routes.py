from events.routes import routes as event_routes
from notes.routes import routes as note_routes
from vault.routes import routes as vault_routes

from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

routes = [
    Mount('/events', routes=event_routes),
    Mount('/notes', routes=note_routes),
    Mount('/vaults', routes=vault_routes),
    Mount('/static', app=StaticFiles(directory='statics'), name='static')
]