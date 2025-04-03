from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import NoteModel, StatusEnum
from .schemas import NoteCreate, Note


async def get_notes(session: AsyncSession, user_id: uuid4):
    query = select(NoteModel).where(NoteModel.user == user_id)
    result = await session.scalars(query)
    notes = result.all()
    return [Note.model_validate(note.__dict__) for note in notes]


async def create_note(session: AsyncSession, data: NoteCreate, user_id: uuid4) -> str | ValueError:
    try:
        note = NoteModel(title=data.title, content=data.content, status=StatusEnum.actual, user=user_id)
        session.add(note)
        await session.commit()
        await session.refresh(note)
        return "Note created successfully"
    except Exception as e:
        await session.rollback()
        raise ValueError(str(e))