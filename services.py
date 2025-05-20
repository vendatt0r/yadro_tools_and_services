import httpx
from sqlmodel import Session, select
from typing import List
from models import User
from db import engine

async def fetch_users(n: int) -> List[User]:
    url = f"https://randomuser.me/api/?results={n}&nat=us,gb,ca"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()["results"]
        users = [
            User(
                gender=u["gender"],
                first_name=u["name"]["first"],
                last_name=u["name"]["last"],
                phone=u["phone"],
                email=u["email"],
                city=u["location"]["city"],
                country=u["location"]["country"],
                thumbnail=u["picture"]["thumbnail"]
            )
            for u in data
        ]
        return users

def save_users(users: List[User]):
    with Session(engine) as session:
        session.add_all(users)
        session.commit()
