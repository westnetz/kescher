import arrow
import hashlib

from kescher.database import get_db
from pathlib import Path
from peewee import (
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
    """
    A Document is an invoice/receipt which reasons a JournalEntry.
    """

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
    """
    A JournalEntry is one row (line) in your imported journal (bank statement).
    """

    date = DateField()
    sender = CharField()
    receiver = CharField()
    subject = CharField()
    document = ForeignKeyField(Document, null=True, backref="journal_entries")
    value = DecimalField()
    balance = DecimalField()
    imported_at = DateTimeField()

    def __str__(self):
        return (
            f"{self.date} | "
            + f"{self.sender[:10]} | "
            + f"{self.receiver[:10]} | "
            + f"{self.subject[:10]} | "
            + f"{self.value}"
        )


class Account(BaseModel):
    """
    Accounts are used to structure bookings e.g. by type, customer, etc.
    """

    name = CharField()
    parent = ForeignKeyField("self", null=True, backref="child_accounts")

    class Meta:
        indexes = ((("name", "parent"), True),)

    def __str__(self):
        return self.name


class Booking(BaseModel):
    """
    A booking references a (partial) amount of a JournalEntry to an Account.
    """

    account = ForeignKeyField(Account, backref="account_entries")
    journalentry = ForeignKeyField(JournalEntry, backref="account_entries")
    comment = CharField(null=True)
    value = DecimalField()

    def __str__(self):
        return (
            f"{self.account} | "
            + f"{self.journalentry} | "
            + f"{self.comment} | "
            + f"{self.value}"
        )


class VirtualBooking(BaseModel):
    """
    To allow for cash accounting, all invoices are to be created as virtual
    account entries.
    """

    account = ForeignKeyField(Account, backref="account_entries")
    date = DateField()
    document = ForeignKeyField(Document, null=True, backref="journal_entries")
    comment = CharField(null=True)
    value = DecimalField()


def create_tables():
    with get_db() as database:
        database.create_tables(
            [Document, JournalEntry, Account, Booking, VirtualBooking]
        )
