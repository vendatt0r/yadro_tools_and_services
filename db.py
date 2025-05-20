from sqlmodel import SQLModel, create_engine
import os
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:123@localhost:5432/yadro_tools")
engine = create_engine(DATABASE_URL, echo=False)

def create_db():
    SQLModel.metadata.create_all(engine)
