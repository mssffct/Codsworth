# import uuid

from litestar import Controller, Request, get

from .schemas import Note
from config import get_logger

logger = get_logger("notesLog", formatter="verbose")


class NotesController(Controller):
    path = "/notes"

    @get("/")
    async def list_notes(self, request: Request) -> dict[str, list[Note]]:
        response = {"items": [Note(id=1, name="test_note")]}
        return response

    @get("/{note_id:int}")
    async def retrieve_note(self, note_id: int) -> Note:
        return Note(id=1, name="test_note")
