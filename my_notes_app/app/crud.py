# app/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas
from fastapi import HTTPException

# Получение заметки по ID
async def get_note_by_id(db: AsyncSession, note_id: int, user_id: int):
    result = await db.execute(select(models.Note).filter(models.Note.id == note_id, models.Note.user_id == user_id))
    return result.scalars().first()

# Создание новой заметки
async def create_note(db: AsyncSession, note: schemas.NoteCreate, user_id: int):
    db_note = models.Note(**note.dict(), user_id=user_id)
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note

# Обновление заметки
async def update_note(db: AsyncSession, note_id: int, note: schemas.NoteUpdate, user_id: int):
    db_note = await get_note_by_id(db, note_id, user_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    for key, value in note.dict(exclude_unset=True).items():
        setattr(db_note, key, value)
    await db.commit()
    await db.refresh(db_note)
    return db_note

# Удаление заметки
async def delete_note(db: AsyncSession, note_id: int, user_id: int):
    db_note = await get_note_by_id(db, note_id, user_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    await db.delete(db_note)
    await db.commit()

# Поиск заметок по тегам
async def search_notes_by_tags(db: AsyncSession, tags: list, user_id: int):
    result = await db.execute(
        select(models.Note).join(models.Note.tags).filter(models.Tag.name.in_(tags), models.Note.user_id == user_id)
    )
    return result.scalars().all()
