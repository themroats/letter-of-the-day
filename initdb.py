from sqlalchemy import Column, Integer, String, create_engine, engine, Sequence, Date, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session


import os


Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

class Letters(Base):
    __tablename__ = 'letters'
    id = Column(Integer, Sequence('letter_id_seq'), primary_key=True)
    date = Column(Date, nullable=False)
    letter = Column(String(1), nullable=False)

    def __repr__(self):
        return "Letter('%s','%s')" % (self.date, self.letter)



def initdb():
    DATABASE_URL = os.environ.get("DATABASE_URL")
    e = create_engine(
        DATABASE_URL
    )
    Base.metadata.create_all(e)
    return e



engine = initdb()
Session = sessionmaker(bind=engine)
sess = Session()

def get_all_users():
    return sess.query(Users).all()

def get_current_letter():
    return sess.query(Letters).order_by(desc(Letters.date), desc(Letters.id)).first()

import datetime

def set_next_letter(next_letter):
    sess.add(Letters(letter=next_letter, date=datetime.datetime.now()))
    sess.commit()

def get_all_letters():
    return sess.query(Letters).all()