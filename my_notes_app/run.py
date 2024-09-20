import uvicorn
import asyncio
from app.db import init_db  # Импорт функции инициализации базы данных
from docker_manager import run_postgres_container, stop_postgres_container  # Импорт функций управления контейнером

async def start_application():
    await init_db()  # Инициализация базы данных
    # Здесь можно добавить другие стартовые действия

if __name__ == "__main__":
    # Поднятие Docker-контейнера перед запуском приложения
    run_postgres_container()

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_application())  # Запуск базы данных
        # Запуск FastAPI приложения
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    finally:
        # Остановка и удаление контейнера после завершения работы
        stop_postgres_container()

