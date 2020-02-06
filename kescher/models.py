import arrow
import hashlib

from kescher.database import get_db
from pathlib import Path
from peewee import (
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    Field,
    ForeignKeyField,
    Model,
    TextField,
)

class BaseModel(Model):

    updated_at = DateTimeField(null=True)

    class Meta:
        database = get_db()

    def save(self, *args, **kwargs):
        self.updated_at = arrow.now().datetime
        return super().save(*args, **kwargs)


class PathField(Field):
    field_type = "TEXT"

    def db_value(self, value):
        return str(value)

    def python_value(self, value):
        return Path(value)


class Document(BaseModel):
    content = TextField()
    path = CharField(unique=True)
    hash = CharField()

    @staticmethod
    def make_hash(path):
        h = hashlib.sha256()
        with open(path, "rb") as infile:
            chunk = 0
            while chunk != b"":
                chunk = infile.read(1024)
                h.update(chunk)
        return h.hexdigest()


class JournalEntry(BaseModel):
    date = DateField()
    sender = CharField()
    receiver = CharField()
    description = CharField()
    document = ForeignKeyField(Document, null=True, backref="journal_entries")
    value = DecimalField()
    balance = DecimalField()
    imported_at = DateTimeField()


class Account(BaseModel):
    name = CharField()
    parent = ForeignKeyField("self", null=True, backref="children")

    def __str__(self):
        return self.name


class AccountEntry(BaseModel):
    """
    An account contains a part or the whole value of the referenced journalentry.
    """

    account = ForeignKeyField(Account, backref="account_entries")
    journalentry = ForeignKeyField(JournalEntry, backref="account_entries")
    value = DecimalField()


class VirtualAccountEntry(BaseModel):
    """
    To allow for cash accounting, all invoices are to be created as virtual 
    account entries.
    """

    account = ForeignKeyField(Account, backref="account_entries")
    date = DateField()
    document = ForeignKeyField(Document, null=True, backref="journal_entries")
    value = DecimalField()


def create_tables():
    with get_db() as database:
        database.create_tables(
            [Document, JournalEntry, Account, AccountEntry, VirtualAccountEntry]
        )
