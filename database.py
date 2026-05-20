# pyrefly: ignore [missing-import]
from sqlalchemy import create_engine
# pyrefly: ignore [missing-import]
from sqlalchemy.ext.declarative import declarative_base
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import sessionmaker, Session
from typing import Annotated
# pyrefly: ignore [missing-import]
from fastapi import Depends
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
import os

load_dotenv()

URL_POSTGRES = os.getenv("DATABASE_URL")
engine = create_engine(URL_POSTGRES)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def GetDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


dbDependency = Annotated[Session, Depends(GetDB)]
