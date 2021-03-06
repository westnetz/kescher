#!/usr/bin/env python3
import arrow
import click
import logging
import sys

from colorama import init, Fore
from decimal import Decimal
from kescher.booking import (
    auto_book_vat,
    book_entry,
    get_account_saldo,
)
from kescher.filters import (
    BookingFilter,
    JournalFilter,
    UnbalancedFilter,
    VirtualBookingFilter,
)
from kescher.importers import (
    AccountImporter,
    DocumentImporter,
    InvoiceImporter,
    JournalImporter,
)
from kescher.logging import setup_logging
from kescher.models import Account, create_tables
from kescher.show import show_accounts, show_table
from pathlib import Path
from peewee import DoesNotExist

DEFAULT_WIDTH = 80

cwd = Path.cwd()
logger = setup_logging(cwd)
init(autoreset=True)


@click.group()
@click.option(
    "--debug/--no-debug", default=False, help="Activate/Deactive verbose logging."
)
def cli(debug):
    """
    kescher cli allows you to bulk import invoices, journals, accounts and documents. Furthermore
    you can use various reporting functions to get a quick overview over your accounts.
    """
    if debug:
        logger.setLevel(logging.DEBUG)
    logger.debug("Debug mode is on")


@cli.group("import")
def importer():
    """
    Import documents, journal, invoices and accounts.
    """
    pass


@importer.command("journal")
@click.argument("journal_file", type=click.File("r"))
def import_journal(journal_file):
    """
    Import journal entries from csv.
    """
    print(f"Importing CSV journal {journal_file.name}...")
    JournalImporter(journal_file)()


@importer.command("accounts")
@click.argument("account_file", type=click.File("r"))
def import_accounts(account_file):
    """
    Bulk import accounts from yaml file.
    """
    print(f"Importing accounts from file {account_file.name}...")
    AccountImporter(account_file)()


@importer.command("documents")
@click.argument("path", type=click.Path(exists=True))
def import_documents(path):
    """
    Bulk import pdf documents.
    """
    print(f"Importing documents from {path}...")
    DocumentImporter(path)()


@importer.command("invoices")
@click.option("--flat/--nested", default=False, help="Invoices in subdirectories?")
@click.argument("path", type=click.Path(exists=True))
@click.argument("account_key")
@click.argument("amount_key")
@click.argument("date_key")
def import_invoices(flat, path, account_key, amount_key, date_key):
    """
    Bulk import yaml invoices.
    """
    print(f"Import invoices from {path}...")
    InvoiceImporter(path, account_key, amount_key, date_key, flat)()


@cli.group()
def book():
    """
    Book to accounts or automatically book VAT.
    """
    pass


@book.command()
@click.argument("vat_percentage", type=click.INT)
@click.argument("vat_in_acc")
@click.argument("vat_out_acc")
def vat(vat_percentage, vat_in_acc, vat_out_acc):
    """
    Helper to bulk book vat.

    You have to give your default VAT percentage as well as the names of your VAT accounts.
    """
    auto_book_vat(vat_percentage, vat_in_acc, vat_out_acc)


@book.command("entry")
@click.option("--value", "-v", type=Decimal)
@click.option("--comment", "-c")
@click.option("--force", is_flag=True, default=False)
@click.option("--width", type=click.INT, default=DEFAULT_WIDTH)
@click.argument("journalentry")
@click.argument("account")
def entry(value, comment, force, width, journalentry, account):
    """
    Book the absolute value of the non-booked rest of a journalentry to the given account.
    """
    try:
        book_entry(value, comment, journalentry, account, force)
    except ValueError as e:
        sys.exit(e)
    print(Fore.YELLOW + "Entry")
    show_table(JournalFilter(), f"id={journalentry}", width)
    print(Fore.YELLOW + "Bookings")
    show_table(BookingFilter(), f"journalentry_id={journalentry}", width)


@cli.group()
def show():
    """
    Show account saldo, journal or accounts.
    """
    pass


@show.command("account")
@click.argument("account")
@click.option("--width", type=click.INT, default=DEFAULT_WIDTH)
def show_account(account, width):
    acc = Account.get(Account.name == account)
    print(Fore.YELLOW + "Bookings")
    show_table(BookingFilter(), f"account_id={acc.id}", width)
    print(Fore.YELLOW + "VirtualBookings")
    show_table(VirtualBookingFilter(), f"account_id={acc.id}", width)
    print(Fore.YELLOW + "Saldo")
    saldo, virtual_saldo = get_account_saldo(account, with_virtual=True)
    print(f"Booking saldo:\t\t{saldo}")
    print(f"VirtualBooking saldo:\t{virtual_saldo}")


@show.command()
@click.argument("account")
@click.option("--start", default=None)
@click.option("--end", default=None)
@click.option("--with-virtual", default=False)
def saldo(account, start, end, with_virtual):
    """
    Sum account bookings for given time frame.
    """
    if start is not None:
        start = arrow.get(start)
    if end is not None:
        end = arrow.get(end)
    saldo = get_account_saldo(account, start, end, with_virtual)
    print(f"Saldo is {saldo}")


@show.command()
@click.option("--filter", default=None)
@click.option("--width", type=click.INT, default=DEFAULT_WIDTH)
def journal(filter, width):
    """
    Show all journal entries or filter by value.
    """
    show_table(JournalFilter(), filter, width)


@show.command()
@click.option("--width", type=click.INT, default=DEFAULT_WIDTH)
def unbalanced(width):
    """
    Show journal entries where added bookings do not add up to zero.
    """
    show_table(UnbalancedFilter(), None, width)


@show.command()
def accounts():
    """
    List all known accounts
    """
    for layer, name, saldo, virtual_saldo in show_accounts():
        if not virtual_saldo:
            real_saldo = saldo
        else:
            real_saldo = -saldo - virtual_saldo
        if real_saldo < 0:
            print_saldo = Fore.RED + str(real_saldo)
        else:
            print_saldo = Fore.GREEN + str(real_saldo)
        print("┃ " * layer + f"┣━{name} {print_saldo}")


@show.command("entry")
@click.option("--width", type=click.INT, default=DEFAULT_WIDTH)
@click.argument("entry_id")
def show_entry(width, entry_id):
    """
    Show a journal entry and all corresponding bookings.
    """
    print(Fore.YELLOW + "Entry")
    show_table(JournalFilter(), f"id={entry_id}", width)
    print(Fore.YELLOW + "Bookings")
    show_table(BookingFilter(), f"journalentry_id={entry_id}", width)


@cli.command("init")
def initialize():
    """
    Create the database in the current working directory.
    """
    print("Setting up database and directories...")
    create_tables()


@cli.group()
def create():
    """
    Create accounts
    """
    pass


@create.command("account")
@click.option("--parent", default=None)
@click.argument("name")
def create_account(parent, name):
    parent_account = None
    if parent:
        try:
            parent_account = Account.get(Account.name == parent)
        except DoesNotExist:
            sys.exit(f"Parent account {parent} not found.")
    if parent_account:
        new_acc = Account.get_or_create(name=name, parent=parent_account)
    else:
        new_acc = Account.get_or_create(name=name)
    if new_acc[1]:
        print(f"New account created: {new_acc[0]}")
    else:
        print(f"Account already exists: {new_acc[0]}")
