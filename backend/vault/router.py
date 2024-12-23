from litestar import Router

from .views import list_vaults


vaults_router = Router(path="/vaults", route_handlers=[list_vaults])
