from typing import Optional
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    gender: str
    first_name: str
    last_name: str
    phone: str
    email: str
    city: str
    country: str
    thumbnail: str
