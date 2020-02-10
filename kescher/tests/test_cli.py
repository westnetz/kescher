import yaml

from click.testing import CliRunner
from kescher.models import Account, Document, JournalEntry, VirtualBooking
from kescher.cli import cli
from pathlib import Path

KESCHER_DB = "kescher.db"
KESCHER_LOG = "kescher.log"

FIXTURES_PATH = Path("kescher/tests/fixtures")
ACCOUNTS_FILE = FIXTURES_PATH / "accounts.yaml"
JOURNAL_FILE = FIXTURES_PATH / "journal.csv"
INVOICES_FLAT = FIXTURES_PATH / "invoices_flat"
INVOICES_NESTED = FIXTURES_PATH / "invoices_nested"

DOC_HASHES = {
    "1000.2019.Q3.pdf": "254e330461e4a64a4243ff7899ab67a8daf069a1b6fc738d4db1c768df4d26a7",
    "1003.2019.Q3.pdf": "abd6405a9e3b070c83800e2d0fd8057c8592b04fed669837dd9b4ae030d673ae",
    "1003.2019.Q4.pdf": "f3ed252796e9ef1855d3ef87d459c0541ca53e113cac4b549f5401214b9abfc0",
    "1003.2019.Q1.pdf": "6364ff0e9f62e509061ff1b7954cf99fc065033642e3749c1fe1420d613c7c29",
    "1003.2019.Q2.pdf": "03306096ef3acdcefe67ce02bb96322742147277170e5d6d7201702ef2cbb83d",
    "1000.2019.Q4.pdf": "ee8212abea2297611eb1ae88871ff0f5533087bb6d4fb5234f278df3c96c8a1c",
}


def test_init_creates_db_and_log():
    runner = CliRunner()
    result = runner.invoke(cli, ("--debug", "init"))
    assert result.exit_code == 0
    assert Path(KESCHER_DB).is_file()
    assert Path(KESCHER_LOG).is_file()


def test_init_debug_writes_to_log():
    runner = CliRunner()
    result = runner.invoke(cli, ("--debug", "init"))
    assert result.exit_code == 0
    with open(KESCHER_LOG) as logfile:
        log_content = logfile.read()
        assert "kescher - DEBUG - Debug mode is on" in log_content


def test_import_accounts():
    runner = CliRunner()
    result = runner.invoke(cli, ["import-accounts", str(ACCOUNTS_FILE)])
    assert result.exit_code == 0
    output_string = (
        "Importing accounts from file kescher/tests/fixtures/accounts.yaml..."
    )
    assert output_string in result.output
    with open(ACCOUNTS_FILE) as a_file:
        accounts = yaml.safe_load(a_file)
    # Check for correct amount of parent accounts
    assert len(accounts) == Account.select().where(Account.parent_id.is_null()).count()
    for account in iterate_accounts(accounts):
        assert Account.get_or_none(Account.name == account) is not None


def iterate_accounts(accounts):
    if isinstance(accounts, list):
        for account in accounts:
            if isinstance(account, str):
                yield account
            else:
                yield from iterate_accounts(account)
    elif isinstance(accounts, dict):
        for account, children in accounts.items():
            yield account
            yield from iterate_accounts(children)


def test_import_journal():
    runner = CliRunner()
    result = runner.invoke(cli, ["import-journal", str(JOURNAL_FILE)])
    assert result.exit_code == 0
    output_string = "Importing CSV journal kescher/tests/fixtures/journal.csv..."
    assert output_string in result.output
    assert len(JournalEntry.select()) == 6


def test_import_invoices():
    runner = CliRunner()
    result = runner.invoke(
        cli, ["import-invoices", str(INVOICES_NESTED), "cid", "total_gross", "date"]
    )
    assert result.exit_code == 0
    output_string = "Import invoices from kescher/tests/fixtures/invoices_nested..."
    assert output_string in result.output
    assert len(Document.select()) == 6
    result = runner.invoke(
        cli,
        ["import-invoices", "--flat", str(INVOICES_FLAT), "cid", "total_gross", "date"],
    )
    output_string = "Import invoices from kescher/tests/fixtures/invoices_flat..."
    assert output_string in result.output
    assert len(VirtualBooking.select()) == 12
    assert len(Document.select()) == 12
    for doc_name, doc_hash in DOC_HASHES.items():
        for db_doc in Document.select().where(Document.hash == doc_hash):
            assert db_doc.path.endswith(doc_name)


def test_import_document():
    runner = CliRunner()
    result = runner.invoke(cli, ["import-documents", str(INVOICES_FLAT)])
    assert result.exit_code == 0
    output_string = "Importing documents from kescher/tests/fixtures/invoices_flat..."
    assert output_string in result.output
    assert len(Document.select()) == 12
    for doc_name, doc_hash in DOC_HASHES.items():
        for db_doc in Document.select().where(Document.hash == doc_hash):
            assert db_doc.path.endswith(doc_name)
