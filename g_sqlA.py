import sqlalchemy as sqlA
import datetime

DB_engine = sqlA.create_engine('sqlite:///sqlite3.db')
DB_metadata = sqlA.MetaData()

tasks = sqlA.Table('tasks', DB_metadata,
                   sqlA.Column('id' , sqlA.Integer(), primary_key=True),
                   sqlA.Column('created' , sqlA.DateTime(), default=datetime.datetime.now()),
                   sqlA.Column('user_id' , sqlA.Integer(), nullable=False),
                   sqlA.Column('date' , sqlA.Date(), nullable=False),
                   sqlA.Column('time' , sqlA.Time(), nullable=False),
                   sqlA.Column('text' , sqlA.String(100), nullable=False),
                   sqlA.Column('status' , sqlA.String(4), nullable=False)
)

scheduler = sqlA.Table('scheduler', DB_metadata,
                       sqlA.Column('id' , sqlA.Integer(), primary_key=True, autoincrement=True),
                       sqlA.Column('task_id' , sqlA.Integer(), nullable=False),
                       sqlA.Column('time' , sqlA.Time(), nullable=False)
)