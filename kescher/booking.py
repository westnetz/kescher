import logging

from decimal import Decimal
from kescher.database import get_db
from kescher.models import Account, Booking, JournalEntry


def auto_book_vat(percentage, vat_in_acc, vat_out_acc):
    """
    This function automatically books VAT for all journal entries.

    TODO: Filtering by date/range and check for existing bookings
    to prevent double booking.
    """
    logger = logging.getLogger("kescher.booking.auto_book_vat")
    vat_in_id = Account.get(Account.name == vat_in_acc).id
    vat_out_id = Account.get(Account.name == vat_out_acc).id
    for je in JournalEntry.select():
        if je.value > 0:
            with get_db() as db:
                booking_value = round(
                    je.value - (je.value * 100) / (100 + Decimal(percentage)), 2
                )
                Booking.create(
                    value=booking_value, account_id=vat_in_id, journalentry_id=je.id,
                )
                logger.debug(f"Added Booking of {booking_value} to {vat_in_acc}.")
        elif je.value < 0:
            with get_db() as db:
                booking_value = -round(
                    je.value - (je.value * 100) / (100 + Decimal(percentage)), 2
                )
                Booking.create(
                    value=booking_value, account_id=vat_out_id, journalentry_id=je.id,
                )
                logger.debug(f"Added Booking of {booking_value} to {vat_out_acc}.")
