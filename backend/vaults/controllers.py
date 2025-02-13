from litestar import Controller, Request, get

from .instances import Vault


class VaultsController(Controller):
    path = "/vaults"

    @get("/")
    async def list_vaults(self, request: Request) -> Vault:
        return Vault(id=1, name="test_vault")
