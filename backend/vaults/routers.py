from litestar import Router

from .controllers import VaultsController


vaults_router = Router(path="/", route_handlers=[VaultsController])
