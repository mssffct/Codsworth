from starlette.responses import JSONResponse
from starlette.endpoints import HTTPEndpoint


class Event(HTTPEndpoint):

    async def events_list(self, request):
        return JSONResponse({})
