from sqlmodel import SQLModel, create_engine
import os
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./yadro_tools.db")
engine = create_engine(DATABASE_URL, echo=False)

def create_db():
    SQLModel.metadata.create_all(engine)
