#!/usr/bin/env python3

import click
import logging

from kescher.importers import AccountImporter, DocumentImporter, JournalImporter
from kescher.logging import setup_logging
from kescher.models import create_tables, JournalEntry
from pathlib import Path

cwd = Path.cwd()
logger = setup_logging(cwd)


@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    if debug:
        logger.setLevel(logging.DEBUG)
    logger.debug("Debug mode is on")


@cli.command()
@click.argument("journal_file", type=click.File("r"))
def import_journal(journal_file):
    print(f"Importing CSV journal {journal_file.name}...")
    JournalImporter(journal_file)()


@cli.command()
@click.argument("account_file", type=click.File("r"))
def import_accounts(account_file):
    print(f"Importing accounts from file {account_file.name}...")
    AccountImporter(account_file)()


@cli.command()
@click.argument("path", type=click.Path(exists=True))
def import_documents(path):
    print(f"Importing documents from {path}...")
    DocumentImporter(path)()


@cli.command()
def annotate():
    print("Annotating...")
    je = JournalEntry.get(JournalEntry.id == 1)
    je.save()


@cli.command()
def export():
    print("Exporting...")


@cli.command()
def init():
    print("Setting up database and directories...")
    create_tables()
