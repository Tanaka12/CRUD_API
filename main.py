from dotenv import load_dotenv
from fastapi import FastAPI
import os
from sqlalchemy import create_engine
import uvicorn

from API import router as api_router
from Entities import Base
from Services import ContextService

app = FastAPI()

def init_environment():
    load_dotenv()

def init_db():
    engine = create_engine(os.environ.get('DB_CONNECTION'))
    Base.metadata.create_all(engine)

    ContextService.set_item("engine", engine)

def init_router():
    app.include_router(api_router)

if __name__ == '__main__':
    init_environment()
    engine = init_db()
    init_router()

    uvicorn.run(app, host="0.0.0.0", port=8000)