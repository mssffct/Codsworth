from litestar import Controller, Request, get, post, delete
from litestar.exceptions import HTTPException
from litestar.params import Body
from uuid import uuid4
from litestar.status_codes import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import Note, NoteCreate
from .crud import get_notes, create_note, delete_note
from config import get_logger

logger = get_logger("notesLog", formatter="verbose")


class NotesController(Controller):
    path = "/notes"

    @get("/")
    async def list_notes(
        self, db_session: AsyncSession, request: Request
    ) -> dict[str, list[Note]]:
        user_id = request.user.unique_id
        notes = await get_notes(db_session, user_id)
        return {"result": notes}

    @get("/{note_id:int}")
    async def retrieve_note(self, note_id: int) -> Note:
        pass

    @post("/create")
    async def create_note(
        self, db_session: AsyncSession, request: Request, data: NoteCreate = Body()
    ) -> str | HTTPException:
        try:
            response = await create_note(
                session=db_session, data=data, user_id=request.user.unique_id
            )
            return response
        except ValueError as e:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=str(e),
            )

    @delete("/{note_id:str}", status_code=HTTP_204_NO_CONTENT)
    async def delete_note(
        self, db_session: AsyncSession, request: Request, note_id: str
    ) -> None:
        try:
            await delete_note(
                session=db_session, pk=note_id, user_id=request.user.unique_id
            )
        except ValueError as e:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=str(e),
            )
