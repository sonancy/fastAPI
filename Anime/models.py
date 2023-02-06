from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Float
import uuid


class Anime(Base):
    __tablename__ = "Anime"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    title = Column(String)
    episodes = Column(Integer, default=1)
    status = Column(String)
    duration = Column(String)
    ratings = Column(Float)
    # photo = ImageField(upload_to='anime')
    description = Column(String)
    genre_id = Column(String, ForeignKey("Genre.id"))
    user_id = Column(String, ForeignKey("User.id"))
    genres = relationship("Genre", back_populates="anime")
    created_by = relationship("User", back_populates="anime")


class Genre(Base):
    __tablename__ = "Genre"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    name = Column(String)

    user_id = Column(String, ForeignKey("User.id"))
    anime = relationship("Anime", back_populates="genres")
    created_by = relationship("User", back_populates="genre")


class User(Base):
    __tablename__ = 'User'

    id = Column(String, primary_key=True, index=True,
                default=str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    anime = relationship("Anime", back_populates="created_by")
    genre = relationship("Genre", back_populates="created_by")
