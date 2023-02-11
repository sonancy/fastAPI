from sqlalchemy import String, Column, TIMESTAMP, text, ForeignKey
from database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    username = Column(String,  nullable=False, unique=True)
    name = Column(String)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))

    bike = relationship('Bike', back_populates="user")
    like = relationship('Like', back_populates="user")
    comment = relationship('Comment', back_populates="user")
    bike_type = relationship('BikeType', back_populates="user")


class BikeType(Base):
    __tablename__ = 'bike_type'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    name = Column(String, unique=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey(
        "user.id", ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))

    user = relationship('User', back_populates="bike_type")
    bike = relationship('Bike', back_populates="bike_type")


class Bike(Base):
    __tablename__ = 'bike'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    name = Column(String)
    model = Column(String)
    brand = Column(String)
    bike_type_id = Column(UUID(as_uuid=True), ForeignKey(
        "bike_type.id", ondelete='CASCADE'), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey(
        "user.id", ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))

    user = relationship('User', back_populates="bike")
    bike_type = relationship('BikeType', back_populates="bike")
    like = relationship('Like', back_populates="bike")
    comment = relationship('Comment', back_populates="bike")


class Like(Base):
    __tablename__ = "like"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    bike_id = Column(UUID(as_uuid=True), ForeignKey(
        "bike.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="like")
    bike = relationship("Bike", back_populates="like")


class Comment(Base):
    __tablename__ = "comment"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    description = Column(String)
    bike_id = Column(UUID(as_uuid=True), ForeignKey(
        "bike.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="comment")
    bike = relationship("Bike", back_populates="comment")
