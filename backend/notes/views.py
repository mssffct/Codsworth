from litestar import Request, get

from .instances import Note


@get('/')
async def list_notes(request: Request) -> Note:
    return Note(id=1, name="test_note")
