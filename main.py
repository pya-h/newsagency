# main.py
from fastapi import FastAPI, Request, Depends, Form, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
import crud
import models
import schemas
from database import SessionLocal, engine
from fastapi.staticfiles import StaticFiles
import urllib
models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

current_user = None

# Dependency
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def get_home(request: Request, db: Session = Depends(get_db)):
    news = crud.get_items(db)
    # sort
    for i in range(len(news)):
        for j in range(i + 1, len(news)):
            if news[i].view_counter < news[j].view_counter:
                temp = news[i]
                news[i] = news[j]
                news[j] = temp

    classified = {}
    for n in news:
        if not n.item_class in classified:
            classified[n.item_class] = []
        classified[n.item_class].append(n)

    return templates.TemplateResponse("index.html", {"request": request, "news": classified})


@app.get("/+")
async def get_add_new(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("addnew.html", {"request": request, "user": current_user})

@app.get("/news/{news_id}")
async def get_add_new(request: Request, news_id: int, db: Session = Depends(get_db)):
    news_item = crud.get_news_by_id(db, news_id)
    news_item.view_counter += 1
    db.commit()
    return templates.TemplateResponse("news_item.html", {"request": request, "item": news_item})


@app.post("/+")
async def get_add_new(request: Request, title: str = Form(), body: str = Form(), news_class: str = Form(), db: Session = Depends(get_db)):
    crud.create_news(db, title, body, news_class)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/register")
async def get_register(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/login")
async def get_login(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/register")
def register(request: Request, email: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if db_user:
        return templates.TemplateResponse("register.html", {"request": request, "msg": "این ایمیل قبلا استفاده شده است!"})
    new_user = crud.create_user(db=db, email=email, password=password)
    return RedirectResponse(url="/",  status_code=status.HTTP_303_SEE_OTHER)


@app.post("/login")
def login(request: Request, email: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if not db_user:
        return templates.TemplateResponse("login.html", {"request": request, "msg": "چنین کاربری وجود ندارد!"})

    hashed_pass = password + "notreallyhashed"
    if hashed_pass != db_user.hashed_password:
        return templates.TemplateResponse("login.html", {"request": request, "msg": "رمز وارد شده اشتباه است!"})
    return RedirectResponse(url="/",  status_code=status.HTTP_303_SEE_OTHER)