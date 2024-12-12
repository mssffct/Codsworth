from starlette.responses import JSONResponse
from starlette.endpoints import HTTPEndpoint


class Note(HTTPEndpoint):

    async def notes_list(self, request):
        return JSONResponse({})