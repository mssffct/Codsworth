# import uuid

from litestar import Controller, Request, get

from .instances import Note


class NotesController(Controller):
    path = '/notes'

    @get('/')
    async def list_notes(self, request: Request) -> dict[str, list[Note]]:
        response = {"items": [Note(id=1, name="test_note")]}
        return response


    @get('/{note_id:int}')
    async def retrieve_note(self, note_id: int) -> Note:
        return Note(id=1, name="test_note")