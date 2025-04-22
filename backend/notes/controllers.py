from uuid import UUID
from litestar import Controller, Request, get, post, delete, patch
from litestar.exceptions import HTTPException
from litestar.params import Body
from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
)
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import Note, NoteCreate
from .crud import get_notes, create_update_note, move_note_to_trash, retrieve_note
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

    @get("/{note_id:uuid}")
    async def retrieve_note(
        self, db_session: AsyncSession, request: Request, note_id: UUID
    ) -> Note | HTTPException:
        try:
            response = await retrieve_note(
                session=db_session, user_id=request.user.unique_id, pk=note_id
            )
            return response
        except ValueError as e:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail=str(e),
            )

    @post("/create")
    async def create_note(
        self, db_session: AsyncSession, request: Request, data: NoteCreate = Body()
    ) -> str | HTTPException:
        try:
            response = await create_update_note(
                session=db_session, data=data, user_id=request.user.unique_id
            )
            return response
        except ValueError as e:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=str(e),
            )

    @patch("/{note_id:uuid}")
    async def patch_note(
        self, db_session: AsyncSession, request: Request, note_id: UUID, data: NoteCreate = Body()
    ) -> str | HTTPException:
        try:
            response = await create_update_note(
                session=db_session, data=data, user_id=request.user.unique_id, note_id=note_id
            )
            return response
        except ValueError as e:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=str(e),
            )

    @delete("/{note_id:uuid}", status_code=HTTP_204_NO_CONTENT)
    async def delete_note(
        self, db_session: AsyncSession, request: Request, note_id: UUID
    ) -> None:
        """
        Moves note to trash (marks it with 'to_delete' status, so that trash collector
        (upcoming feature) could delete it permanently after the appointed time)
        """
        try:
            await move_note_to_trash(
                session=db_session, pk=note_id, user_id=request.user.unique_id
            )
        except ValueError as e:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail=str(e),
            )
