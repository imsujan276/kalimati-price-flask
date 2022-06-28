from . import db
from sqlalchemy import VARCHAR, Column, Integer, DateTime, String
from sqlalchemy.sql import func

class MyData(db.Model):
    __tablename__ = 'my_data'
    id = db.Column(
        Integer,
        primary_key=True,
        index=False,
    )
    prices = db.relationship(
        'Price', 
        backref='my_data', 
        lazy='dynamic'
    )
    date = db.Column(
        String(),
        nullable=True
    )
    created_date = db.Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self):
        return '<MyData {}>'.format(self.data)

    def to_json(self):
        return {
            'id': self.id,
            'data': self.prices,
            'date': self.date,
            "created_date": self.created_date
        }

class Price(db.Model):
    __tablename__ = 'price'
    id = db.Column(
        Integer,
        primary_key=True,
        index=False,
    )
    title = db.Column(
        String(),
        nullable=True
    )
    unit = db.Column(
        String(),
        nullable=True
    )
    min = db.Column(
        String(),
        nullable=True
    )
    max = db.Column(
        String(),
        nullable=True
    )
    avg = db.Column(
        String(),
        nullable=True
    )
    my_data_id = db.Column(db.Integer, db.ForeignKey('my_data.id'))

    def __repr__(self):
        return f'<Price "{self.title[:20]}...">'

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'unit': self.unit,
            'min': self.min,
            'max': self.max,
            'avg': self.avg,
        }