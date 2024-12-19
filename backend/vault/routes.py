from starlette.routing import Route

from .views import Vault

routes = [
    Route('/', Vault),
]
