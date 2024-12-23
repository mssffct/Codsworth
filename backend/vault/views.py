from litestar import Request, get

from .instances import Vault


@get('/')
async def list_vaults(request: Request) -> Vault:
    return Vault(id=1, name="test_vault")
