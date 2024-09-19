import uvicorn
import asyncio
from app.db import db  # Import your database initialization function

async def start_application():
    await db()  # Initialize your database
    # Here, you can add any other startup logic if needed

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_application())  # Start the database
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
