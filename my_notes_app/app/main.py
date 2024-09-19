
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_302_FOUND
from app import models, crud, schemas, auth
from app.db import engine, get_db
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

# Инициализация базы данных
models.Base.metadata.create_all(bind=engine)

# Инициализация приложения FastAPI
app = FastAPI()

# Инициализация шаблонизатора Jinja2
templates = Jinja2Templates(directory="app/templates")

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Маршрут для логина и получения токена
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )
    access_token = auth.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Web-интерфейс для работы с заметками --- #

# Маршрут для отображения всех заметок пользователя
@app.get("/notes", response_class=HTMLResponse)
async def get_notes(request: Request, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    notes = await crud.get_notes_for_user(db, user_id=current_user.id)
    return templates.TemplateResponse("notes.html", {"request": request, "notes": notes})

# Маршрут для создания новой заметки через веб-интерфейс
@app.get("/notes/new", response_class=HTMLResponse)
async def new_note_form(request: Request):
    return templates.TemplateResponse("new_note.html", {"request": request})

# Обработка формы создания новой заметки
@app.post("/notes/new", response_class=HTMLResponse)
async def create_note_via_web(request: Request, title: str = Form(...), content: str = Form(...), tags: str = Form(...), 
                              db: AsyncSession = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    tags_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
    note_data = schemas.NoteCreate(title=title, content=content, tags=tags_list)
    await crud.create_note(db=db, note=note_data, user_id=current_user.id)
    return RedirectResponse(url="/notes", status_code=HTTP_302_FOUND)

# Маршрут для просмотра деталей заметки
@app.get("/notes/{note_id}", response_class=HTMLResponse)
async def read_note(request: Request, note_id: int, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    note = await crud.get_note_by_id(db=db, note_id=note_id, user_id=current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return templates.TemplateResponse("note_detail.html", {"request": request, "note": note})

# Маршрут для поиска заметок по тегам через веб-интерфейс
@app.get("/notes/search", response_class=HTMLResponse)
async def search_notes(request: Request, tags: str, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    tags_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
    notes = await crud.search_notes_by_tags(db=db, tags=tags_list, user_id=current_user.id)
    return templates.TemplateResponse("notes.html", {"request": request, "notes": notes})

# --- API эндпоинты для работы с заметками --- #

# Создание заметки через API
@app.post("/api/notes/", response_model=schemas.NoteResponse)
async def create_note_api(note: schemas.NoteCreate, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return await crud.create_note(db=db, note=note, user_id=current_user.id)

# Получение заметки по ID через API
@app.get("/api/notes/{note_id}", response_model=schemas.NoteResponse)
async def read_note_api(note_id: int, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    note = await crud.get_note_by_id(db=db, note_id=note_id, user_id=current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# Поиск заметок по тегам через API
@app.get("/api/notes/search", response_model=List[schemas.NoteResponse])
async def search_notes_api(tags: List[str], db: AsyncSession = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return await crud.search_notes_by_tags(db=db, tags=tags, user_id=current_user.id)