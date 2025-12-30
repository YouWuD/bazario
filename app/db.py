import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

connect_args = {}
engine_kwargs = {"echo": False, "pool_pre_ping": True}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    engine_kwargs.pop("pool_pre_ping")

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    **engine_kwargs,
)

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# FastAPI app (used for mounting static files)
app = FastAPI(title="Bazario API")

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
