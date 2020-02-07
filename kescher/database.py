from peewee import SqliteDatabase

KESCHER_DB_NAME = "kescher.db"


def get_db():
    return SqliteDatabase(KESCHER_DB_NAME)
