import sqlalchemy as sqlA

DB_engine = sqlA.create_engine('sqlite:///sqlite3.db')
DB_engine.connect()

print(DB_engine)
