import logging

from decimal import Decimal
from kescher.models import Account, Booking, JournalEntry
from peewee import fn


def auto_book_vat(percentage, vat_in_acc, vat_out_acc):
    """
    This function automatically books VAT for all journal entries.

    TODO: Filtering by date/range and check for existing bookings
    to prevent double booking.
    """
    logger = logging.getLogger("kescher.booking.auto_book_vat")
    vat_in_id = Account.get(Account.name == vat_in_acc).id
    vat_out_id = Account.get(Account.name == vat_out_acc).id
    journalentries_with_vat = [
        b.journalentry
        for b in Booking.select().where(
            (Booking.account == vat_in_id) | (Booking.account == vat_out_id)
        )
    ]
    for je in JournalEntry.select():
        if je in journalentries_with_vat:
            print(f"VAT already booked for {je.id} ({je.date})")
            continue
        if je.value > 0:
            booking_value = round(
                je.value - (je.value * 100) / (100 + Decimal(percentage)), 2
            )
            Booking.create(
                value=booking_value, account_id=vat_in_id, journalentry_id=je.id,
            )
            logger.debug(f"Added Booking of {booking_value} to {vat_in_acc}.")
        elif je.value < 0:
            booking_value = -round(
                je.value - (je.value * 100) / (100 + Decimal(percentage)), 2
            )
            Booking.create(
                value=booking_value, account_id=vat_out_id, journalentry_id=je.id,
            )
            logger.debug(f"Added Booking of {booking_value} to {vat_out_acc}.")


def get_account_saldo(account, start_date, end_date):
    saldo = (
        Booking.select(fn.SUM(Booking.value))
        .join(Account)
        .switch(Booking)
        .join(JournalEntry)
        .where(
            (Account.name == account)
            & (JournalEntry.date >= start_date.datetime)
            & (JournalEntry.date <= end_date.datetime)
        )
        .scalar()
    )
    return round(saldo, 2)
