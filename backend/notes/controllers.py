from litestar import Controller, Request, get, post
from litestar.exceptions import HTTPException
from litestar.params import Body
from litestar.status_codes import HTTP_400_BAD_REQUEST
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import Note, NoteCreate
from .crud import get_notes, create_note
from config import get_logger

logger = get_logger("notesLog", formatter="verbose")


class NotesController(Controller):
    path = "/notes"

    @get("/")
    async def list_notes(self, db_session: AsyncSession, request: Request) -> dict[str, list[Note]]:
        user_id = request.user.unique_id
        notes = await get_notes(db_session, user_id)
        return {"result": notes}

    @get("/{note_id:int}")
    async def retrieve_note(self, note_id: int) -> Note:
        return Note(id=1, name="test_note")

    @post("/create")
    async def create_note(self, db_session: AsyncSession, request: Request, data: NoteCreate = Body()) -> str | HTTPException:
        try:
            response = await create_note(db_session, data, request.user.unique_id)
            return response
        except ValueError as e:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=str(e),
            )