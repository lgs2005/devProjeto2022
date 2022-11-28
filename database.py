from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Callable

from flask_jwt_extended import get_current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped

db = SQLAlchemy()

if TYPE_CHECKING:
    import sqlalchemy.orm

    class AppDatabase(SQLAlchemy):
        session: sqlalchemy.orm.scoped_session
    db: AppDatabase


def extract_fields(*fields: str) -> Callable[[object], dict]:
    def dado(o: object, c: str):
        v = o.__getattribute__(c)
        if isinstance(v, datetime):
            v = v.isoformat()

        return v
    return lambda self: {c: dado(self, c) for c in fields}


class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = Column(Integer, primary_key=True)

    name: Mapped[str] = Column(String(255), nullable=False)
    email: Mapped[str] = Column(String(255), nullable=False, unique=True)
    pwhash: Mapped[str] = Column(String(60), nullable=False)

    data = extract_fields('id', 'name', 'email')
    current: Callable[[], User] = lambda: get_current_user()


class Folder(db.Model):
    __tablename__ = 'folder'

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(255), nullable=False)

    user_id: Mapped[int] = Column(ForeignKey(User.id))
    user: Mapped[User] = db.relationship('User')

    pages: Mapped[list[Page]] = db.relationship(
        'Page', back_populates='folder')

    data = extract_fields('id', 'name')


class Page(db.Model):
    __tablename__ = 'page'

    id: Mapped[int] = Column(Integer, primary_key=True)
    author_id: Mapped[int] = Column(ForeignKey(User.id), nullable=False)
    folder_id: Mapped[int] = Column(ForeignKey(Folder.id), nullable=False)

    author: Mapped[User] = db.relationship('User')
    folder: Mapped[Folder] = db.relationship('Folder', back_populates='pages')

    name: Mapped[str] = Column(String(255), nullable=False)
    file: Mapped[str] = Column(String(32), nullable=False)

    creation_date: Mapped[datetime] = Column(DateTime, nullable=False)
    deletion_date: Mapped[datetime] = Column(DateTime)  # nullable

    data = extract_fields('id', 'author_id', 'folder_id',
                          'name', 'file', 'creation_date', 'deletion_date')


class Access(db.Model):
    __tablename__ = 'access'

    user_id: Mapped[int] = Column(ForeignKey(User.id), primary_key=True)
    page_id: Mapped[int] = Column(ForeignKey(Page.id), primary_key=True)

    user: Mapped[User] = db.relationship('User')
    page: Mapped[Page] = db.relationship('Page')

    expiry_date = Column(DateTime, nullable=True)
