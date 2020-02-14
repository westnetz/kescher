#!/usr/bin/env python3
"""
This script sanitizes CSV files downloaded from Postbank (Germany).
It strips useless characters, and converts the numbers to a reasonable
and usable format.
"""
import click
import csv
import locale
import logging

from decimal import Decimal
from kescher.logging import setup_logging
from pathlib import Path

LOCALE = "de_DE.UTF-8"
DECIMAL_QUANTIZATION = ".01"

logger = setup_logging(Path.cwd())


class PostBankCsvParser:

    expected_header = [
        "Buchungsdatum",
        "Wertstellung",
        "Umsatzart",
        "Buchungsdetails",
        "Auftraggeber",
        "Empfänger",
        "Betrag (\x80)",
        "Saldo (\x80)",
    ]

    def __init__(self, q):
        self.q = q

    def header_ok(self, header):
        if header != self.expected_header:
            return False
        return True

    def amount_to_decimal(self, value):
        value = value.replace("\x80", "")
        return Decimal.from_float(locale.atof(value)).quantize(Decimal(self.q))

    def sanitize_subject(self, subject):
        return subject.replace("Referenz NOTPROVIDED", "").replace(
            "Verwendungszweck", ""
        )

    def get_entry(self, row):
        return [
            row[0],
            row[4],
            row[5],
            self.sanitize_subject(row[3]),
            self.amount_to_decimal(row[6]),
            self.amount_to_decimal(row[7]),
        ]


class CsvHeaderError(Exception):
    pass


@click.command()
@click.option("--debug", is_flag=True, default=False, help="Debug logging")
@click.option("--reverse", is_flag=True, default=False, help="Reverse order of rows")
@click.argument("infile", type=click.File("r", encoding="latin3"))
@click.argument("outfile", type=click.File("w"))
def sanitize_postbank(debug, reverse, infile, outfile):
    """
    Helper to convert the shitty CSV files you get from Postbank (Germany)
    into a somewhat reasonable format we can work with. Please give
    an input and an output file as arguments.
    """
    if debug:
        logger.setLevel(logging.DEBUG)
    logger.debug(f"Infile for Postbank Sanitation: {infile.name}")
    logger.debug(f"Outfile for Postbank Sanitation: {outfile.name}")
    pb_csv_parser = PostBankCsvParser(DECIMAL_QUANTIZATION)
    locale.setlocale(locale.LC_ALL, LOCALE)
    reader = csv.reader(infile, quotechar='"', delimiter=";")
    writer = csv.writer(
        outfile, quotechar='"', delimiter=";", quoting=csv.QUOTE_MINIMAL
    )

    rows = []
    for row in reader:
        rows.append(pb_csv_parser.get_entry(row))
        logger.debug(f"Reading row: {', '.join(row)}")

    if reverse:
        rows.reverse()
        logger.debug(f"Reversing result, beause reverse is True")

    writer.writerows(rows)
