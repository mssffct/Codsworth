from starlette.responses import JSONResponse
from starlette.endpoints import HTTPEndpoint


class Vault(HTTPEndpoint):

    async def deposit_boxes_list(self, request):
        return JSONResponse({})