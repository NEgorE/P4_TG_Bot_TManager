import sqlalchemy as sqlA
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import datetime

db_str = 'sqlite:///sqlite3.db'
DB_engine = sqlA.create_engine(db_str)
DB_Base = declarative_base()
DB_metadata = sqlA.MetaData()
session = Session()
class Task(DB_Base):
    __tablename__ = 'tasks'
    id = sqlA.Column(sqlA.Integer(), primary_key=True)
    created = sqlA.Column(sqlA.DateTime(), default=datetime.datetime.now())
    user_id = sqlA.Column(sqlA.Integer(), nullable=False)
    date = sqlA.Column(sqlA.Date(), nullable=False)
    time = sqlA.Column(sqlA.Time(), nullable=False)
    text = sqlA.Column(sqlA.String(100), nullable=False)
    status = sqlA.Column(sqlA.String(4), nullable=False)
class User(DB_Base):
    __tablename__ = 'users'
    id = sqlA.Column(sqlA.Integer(), primary_key=True, autoincrement=True)
    username = sqlA.Column(sqlA.Integer(), nullable=False)
    last_name = sqlA.Column(sqlA.String(20), nullable=True)
    first_name = sqlA.Column(sqlA.String(120), nullable=False)
    language_code = sqlA.Column(sqlA.String(3), nullable=True)
class Sched_item(DB_Base):
    __tablename__ = 'scheduler'
    id = sqlA.Column(sqlA.Integer(), primary_key=True, autoincrement=True)
    task_id = sqlA.Column(sqlA.Integer(), nullable=False)
    time = sqlA.Column(sqlA.Time(), nullable=False)


def db_init():
    DB_Base.metadata.create_all(DB_engine)
    print('DB init done!!!')
    sb_session_open()
    
def sb_session_open():
    global session
    session = Session(bind=DB_engine)
    print('Session is open!!!')

    #def __init__(self, db_str) -> None:
    #    
    #    
    #    
    #    print('DB init done!!!')
    #    self.open_session()
#
    #def open_session(self) :
    #    self.session = Session(bind=self.DB_engine)
    #    print('Session is open!!!')
#
    #def __del__(self) :
    #    print('DB class was delete !!!')