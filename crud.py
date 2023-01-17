from sqlalchemy.orm import Session

import models
import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, email: str, password: str):
    fake_hashed_password = password + "notreallyhashed"
    db_user = models.User(email=email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_news(db: Session, title: str, body: str, news_class: str):
    item = models.Item(title=title, item_class=news_class, body=body, view_counter=0)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_user_classes(db: Session, user_id: int, classes: list[str]):
    db.query(models.User).filter(models.User.id == user_id).update(values={"classes": classes.__str__()})
    db.commit()
    return get_user(db, user_id)


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_news_by_id(db: Session, news_id: int):
    return db.query(models.Item).filter(models.Item.id == news_id).first()


def get_classes_from_str(list_as_str: str):
    list_as_str = list_as_str.replace('[', '').replace(']', '').replace('\'', '').replace(" ", "")
    classes = list_as_str.split(',')
    return classes


