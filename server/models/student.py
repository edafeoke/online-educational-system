#!/usr/bin/python3

from models.base_model import BaseModel, Base
from os import getenv
# import sqlalchemy
from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

HBNB_TYPE_STORAGE = getenv('HBNB_TYPE_STORAGE') or 'file'


class Student(BaseModel, Base):
    '''Student class'''

    __tablename__ = 'students'

    if HBNB_TYPE_STORAGE == 'db':
        email = Column(String(256), nullable=False)
        firstname = Column(String(256), nullable=False)
        lastname = Column(String(256), nullable=False)
        # user_id = Column(String(256),  ForeignKey('users.id'), nullable=False)


    def __init__(self, *args, **kwargs):
    #     """initializes student"""
        self.email = ''
        self.lastname = ''
        self.firstname = ''
        super().__init__(*args, **kwargs)
