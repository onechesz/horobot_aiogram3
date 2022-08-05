from sqlalchemy import Column, Integer, VARCHAR

from .base import BaseModel


class Users(BaseModel):
    __tablename__ = 'users'
    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    zodiac_sign = Column(VARCHAR(8), nullable=True)

    def __str__(self) -> str:
        return f'User: {self.user_id}'
