#!/usr/bin/env python3
import arrow
import click
import logging
import sys

from kescher.booking import auto_book_vat, get_account_saldo
from kescher.importers import (
    AccountImporter,
    DocumentImporter,
    InvoiceImporter,
    JournalImporter,
)
from kescher.helpers import Box
from kescher.logging import setup_logging
from kescher.models import create_tables
from kescher.show import show_accounts, show_journal
from pathlib import Path

cwd = Path.cwd()
logger = setup_logging(cwd)


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


@cli.command()
@click.argument("vat_percentage", type=click.INT)
@click.argument("vat_in_acc")
@click.argument("vat_out_acc")
def auto_vat(vat_percentage, vat_in_acc, vat_out_acc):
    """
    Helper to bulk book vat.
    """
    auto_book_vat(vat_percentage, vat_in_acc, vat_out_acc)


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
@click.option("--width", type=click.INT, default=80)
def journal(filter, width):
    box_helper = None
    try:
        for entry in show_journal(filter, width):
            if not box_helper:
                box_helper = Box([len(e) for e in entry])
                print(box_helper.top())
            else:
                print(box_helper.center())
            print(box_helper.content(entry))
        print(box_helper.bottom())

    except ValueError as e:
        sys.exit(e)


@show.command()
def accounts():
    """
    List all known accounts
    """
    for acc in show_accounts():
        print(acc)


@cli.command()
def init():
    """
    Create the database in the current working directory.
    """
    print("Setting up database and directories...")
    create_tables()
