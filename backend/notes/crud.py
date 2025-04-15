from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from db_utils import atomic
from .models import NoteModel, StatusEnum
from .schemas import NoteCreate, Note


async def get_notes(session: AsyncSession, user_id: uuid4):
    query = select(NoteModel).where(NoteModel.user == user_id)
    result = await session.scalars(query)
    notes = result.all()
    return [Note.model_validate(note.__dict__) for note in notes]


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
async def delete_note(session: AsyncSession, pk: uuid4, user_id) -> str | ValueError:
    filter_kwargs = {"unique_id": pk, "user": str(user_id)}
    try:
        query = select(NoteModel).filter_by(**filter_kwargs)
        result = await session.scalars(query)
        await session.delete(result.first())
        return "OK"
    except Exception as e:
        raise ValueError("!!!")
