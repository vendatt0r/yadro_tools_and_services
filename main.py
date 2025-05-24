from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import func
from sqlmodel import Session, select
from random import choice

from models import User
from db import engine, create_db
from services import fetch_users, save_users

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    create_db()
    with Session(engine) as session:
        if not session.exec(select(User)).first():
            users = await fetch_users(1000)
            save_users(users)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, page: int = 1, per_page: int = 20):
    with Session(engine) as session:
        total = session.exec(select(func.count()).select_from(User)).one()
        users = session.exec(
            select(User).offset((page - 1) * per_page).limit(per_page)
        ).all()
        return templates.TemplateResponse("index.html", {
            "request": request,
            "users": users,
            "page": page,
            "total_pages": (total // per_page) + 1
        })

@app.get("/random", response_class=HTMLResponse)
def random_user(request: Request):
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        user = choice(users)
        return templates.TemplateResponse("user_detail.html", {
            "request": request,
            "user": user
        })

@app.get("/{user_id}", response_class=HTMLResponse)
def read_user(request: Request, user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return templates.TemplateResponse("user_detail.html", {"request": request, "user": user})
