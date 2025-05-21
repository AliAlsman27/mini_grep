from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv(".env")
from routes import base, data
from helpers.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient



from helpers.config import get_settings




app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    """
    Startup event to connect to the database.
    """
    settings = get_settings()
    app.mongodb_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.MONGODB_DB]

@app.on_event("shutdown")
async def shutdown_db_client():
    """
    Shutdown event to close the database connection.
    """
    app.mongodb_client.close()

app.include_router(base.base_router)
app.include_router(data.data_router)