import sqlalchemy as sqlA
import datetime

class DBclass :

    def __init__(self, db_str) -> None:
        
        DB_engine = sqlA.create_engine(db_str)
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
        users = sqlA.Table('users', DB_metadata,
                            sqlA.Column('id' , sqlA.Integer(), primary_key=True, autoincrement=True),
                            sqlA.Column('username' , sqlA.Integer(), nullable=False),
                            sqlA.Column('last_name' , sqlA.String(20), nullable=True),
                            sqlA.Column('first_name' , sqlA.String(120), nullable=False),
                            sqlA.Column('language_code' , sqlA.String(3), nullable=True)
        )

        DB_metadata.create_all(DB_engine)
        print('DB init done!!!')

    def __del__(self) :
        print('DB class was delete !!!')