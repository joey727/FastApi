from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, text
from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone='True'),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "users.user_id", ondelete="CASCADE"), nullable=False)


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone='True'),
                        nullable=False, server_default=text('now()'))
