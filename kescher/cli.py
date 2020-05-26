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
from kescher.filters import EntryFilter, JournalFilter
from kescher.importers import (
    AccountImporter,
    DocumentImporter,
    InvoiceImporter,
    JournalImporter,
)
from kescher.logging import setup_logging
from kescher.models import create_tables
from kescher.show import show_accounts, show_table
from pathlib import Path

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
@click.argument("journalentry")
@click.argument("account")
def entry(value, comment, journalentry, account):
    """
    Book the absolute value of the non-booked rest of a journalentry to the given account.
    """
    try:
        book_entry(value, comment, journalentry, account)
    except ValueError as e:
        sys.exit(e)


@cli.group()
def show():
    """
    Show account saldo, journal or accounts.
    """
    pass


@show.command()
@click.argument("account")
@click.argument("start_date")
@click.argument("end_date")
def saldo(account, start_date, end_date):
    """
    Sum account bookings for given time frame.
    """
    start = arrow.get(start_date)
    end = arrow.get(end_date)
    saldo = get_account_saldo(account, start, end)
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
def accounts():
    """
    List all known accounts
    """
    for acc in show_accounts():
        print(acc)


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
    show_table(EntryFilter(), f"journalentry_id={entry_id}", width)


@cli.command("init")
def initialize():
    """
    Create the database in the current working directory.
    """
    print("Setting up database and directories...")
    create_tables()
