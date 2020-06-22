import logging

from decimal import Decimal
from kescher.models import Account, Booking, JournalEntry, VirtualBooking
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


def book_entry(value, comment, journalentry_id, account_name):
    """
    Book a journalentry to some account.
    """
    logger = logging.getLogger("kescher.booking.auto_book_vat")
    account = Account.get(Account.name == account_name)
    journalentry = JournalEntry.get_by_id(journalentry_id)
    booked = (
        Booking.select(fn.SUM(Booking.value))
        .where(Booking.journalentry == journalentry)
        .scalar()
    )

    remaining = abs(journalentry.value) - Decimal(booked)
    if not remaining:
        raise ValueError("No remaining value to be booked")

    # If no value is given the remaining value is booked (default),
    # i.e. no split booking
    if value is None:
        value_to_book = remaining
    else:
        if value > remaining:
            raise ValueError(f"Cannot book {value}, as only {remaining} is available.")
        else:
            value_to_book = value

    logger.info(f"Booking {value} from of {journalentry.id} to {account.name}")

    new_booking = Booking.create(
        account=account, journalentry=journalentry, value=value_to_book, comment=comment
    )

    return new_booking


def get_account_saldo(account, start_date=None, end_date=None, with_virtual=False):
    stmt = (
        Booking.select(fn.SUM(Booking.value))
        .join(Account)
        .switch(Booking)
        .join(JournalEntry)
    )
    if start_date and end_date:
        stmt = stmt.where(
            (Account.name == account)
            & (JournalEntry.date >= start_date.datetime)
            & (JournalEntry.date <= end_date.datetime)
        )
    else:
        stmt = stmt.where((Account.name == account))
    saldo = stmt.scalar()
    if saldo is None:
        saldo = Decimal("0.0")

    if with_virtual:
        virtual_stmt = (
            VirtualBooking.select(fn.SUM(VirtualBooking.value))
            .join(Account)
            .switch(VirtualBooking)
        )
        if start_date and end_date:
            virtual_stmt = virtual_stmt.where(
                (Account.name == account)
                & (VirtualBooking.date >= start_date.datetime)
                & (VirtualBooking.date <= end_date.datetime)
            )
        else:
            virtual_stmt = virtual_stmt.where((Account.name == account))
        virtual_saldo = virtual_stmt.scalar()
        if virtual_saldo is None:
            saldo = Decimal("0.0")
        return (round(saldo, 2), round(virtual_saldo, 2))
    else:
        return round(saldo, 2)
