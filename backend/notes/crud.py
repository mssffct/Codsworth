import datetime
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from db_utils import atomic
from .models import NoteModel, StatusEnum
from .schemas import NoteCreate, Note
from shared_schemas import Status


async def get_notes(session: AsyncSession, user_id: uuid4) -> list[Note]:
    query = select(NoteModel).where(
        NoteModel.user == user_id, NoteModel.status != Status.to_delete
    )
    result = await session.scalars(query)
    notes = result.all()
    if len(notes) > 0:
        return [Note.model_validate(note.__dict__) for note in notes]
    else:
        return []


async def retrieve_note(
    session: AsyncSession, pk: uuid4, user_id: uuid4
) -> Note | ValueError:
    filter_kwargs = {"unique_id": pk, "user": str(user_id)}
    query = select(NoteModel).filter_by(**filter_kwargs)
    result = await session.scalars(query)
    if note := result.one_or_none():
        return Note.model_validate(note.__dict__)
    else:
        raise ValueError("Cannot retrieve note!")


@atomic()
async def create_note(
    session: AsyncSession, data: NoteCreate, user_id: uuid4
) -> str | ValueError:
    note = NoteModel(
        title=data.title, content=data.content, status=StatusEnum.actual, user=user_id
    )
    session.add(note)
    return "Note created successfully"


@atomic()
async def move_note_to_trash(
    session: AsyncSession, pk: uuid4, user_id
) -> str | ValueError:
    filter_kwargs = {"unique_id": pk, "user": str(user_id)}
    query = (
        update(NoteModel)
        .filter_by(**filter_kwargs)
        .values(status=Status.to_delete, status_date=datetime.datetime.now())
    )
    try:
        await session.execute(query)
        return "OK"
    except Exception:
        raise ValueError("Cannot delete note!")
