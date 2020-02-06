from peewee import SqliteDatabase

KESCHER_DB_NAME = "kescher.db"


def get_db(path=None):
    if not path:
        return SqliteDatabase(KESCHER_DB_NAME)
    else:
        return SqliteDatabase(path / KESCHER_DB_NAME)
