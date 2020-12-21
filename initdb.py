from sqlalchemy import (
    Column,
    Integer,
    String,
    create_engine,
    engine,
    Sequence,
    Date,
    desc,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from flask_login import UserMixin, current_user


import os


Base = declarative_base()


class Users(Base, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    username = Column(String(50))
    password = Column(String(100))

    def __repr__(self):
        return "<User('%s', '%s')>" % (self.username, self.password)


class Letters(Base):
    __tablename__ = "letters"
    id = Column(Integer, Sequence("letter_id_seq"), primary_key=True)
    date = Column(Date, nullable=False)
    letter = Column(String(1), nullable=False)

    def __repr__(self):
        return "Letter('%s','%s')" % (self.date, self.letter)


class Votes(Base):
    __tablename__ = "votes"
    id = Column(Integer, Sequence("vote_id_seq"), primary_key=True)
    letter_id = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    username = Column(String(50))

    def __repr__(self):
        return "Vote('%s','%s','%s')" % (self.letter_id, self.score, self.username)


def initdb():
    DATABASE_URL = os.environ.get("DATABASE_URL")
    e = create_engine(DATABASE_URL)
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


def vote_letter(change):
    letter = get_current_letter()
    score = 1 if change == "up" else -1
    prev_vote = sess.query(Votes).filter_by(username=current_user.username, letter_id=letter.id).first()
    if prev_vote:
        prev_vote.score = score
    else:
        sess.add(Votes(letter_id=letter.id, username=current_user.username, score=score))
    sess.commit()


def get_letter_score(id):
    return sess.query(func.sum(Votes.score)).filter_by(letter_id=id).first()[0]