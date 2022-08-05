from sqlalchemy import Column, VARCHAR

from .base import BaseModel


class Horoscope(BaseModel):
    __tablename__ = 'horoscope'
    zodiac_sign = Column(VARCHAR(8), nullable=True, primary_key=True)
    horoscope_daily = Column(VARCHAR(1000), nullable=True)
    horoscope_tomorrow = Column(VARCHAR(1000), nullable=True)
    horoscope_weekly = Column(VARCHAR(1000), nullable=True)

    def __str__(self):
        return f'Zodiac sign: {self.zodiac_sign}'
