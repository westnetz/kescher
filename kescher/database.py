from peewee import SqliteDatabase

def get_db():
    return SqliteDatabase("kescher.db")

