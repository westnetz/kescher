"""
This module contains the tests for cli commands. It asserts that the
command line interface works as intended.
"""
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
    """
    Asserts that a database file and a log file is created and the
    init command exits with 0 as exit_code.
    """
    runner = CliRunner()
    result = runner.invoke(cli, ("--debug", "init"))
    assert result.exit_code == 0
    assert Path(KESCHER_DB).is_file()
    assert Path(KESCHER_LOG).is_file()


def test_init_debug_writes_to_log():
    """
    Asserts that the --debug flag turns on debug messages to be written to the log.
    """
    runner = CliRunner()
    result = runner.invoke(cli, ("--debug", "init"))
    assert result.exit_code == 0
    with open(KESCHER_LOG) as logfile:
        log_content = logfile.read()
        assert "kescher - DEBUG - Debug mode is on" in log_content


def test_import_accounts():
    """
    Asserts that a set of test accounts are imported correctly.
    """
    runner = CliRunner()
    result = runner.invoke(cli, ["import", "accounts", str(ACCOUNTS_FILE)])
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
    """
    Helper function to iterate to ease iterating through the accounts.
    """
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
    """
    Asserts that a test journal is imported correctly and the import exits
    with 0 as exit code.
    """
    runner = CliRunner()
    result = runner.invoke(cli, ["import", "journal", str(JOURNAL_FILE)])
    assert result.exit_code == 0
    output_string = "Importing CSV journal kescher/tests/fixtures/journal.csv..."
    assert output_string in result.output
    assert len(JournalEntry.select()) == 6


def test_import_invoices():
    """
    Asserts that invoices are imported correctly, connected pdf documents are
    imported as well and the command exits with 0 as exit code. The invoices
    import is perfomed for the nested and flat directory structure.
    """
    runner = CliRunner()
    result = runner.invoke(
        cli, ["import", "invoices", str(INVOICES_NESTED), "cid", "total_gross", "date"]
    )
    assert result.exit_code == 0
    output_string = "Import invoices from kescher/tests/fixtures/invoices_nested..."
    assert output_string in result.output
    assert len(Document.select()) == 6
    result = runner.invoke(
        cli,
        [
            "import",
            "invoices",
            "--flat",
            str(INVOICES_FLAT),
            "cid",
            "total_gross",
            "date",
        ],
    )
    output_string = "Import invoices from kescher/tests/fixtures/invoices_flat..."
    assert output_string in result.output
    assert len(VirtualBooking.select()) == 12
    assert len(Document.select()) == 12
    for doc_name, doc_hash in DOC_HASHES.items():
        for db_doc in Document.select().where(Document.hash == doc_hash):
            assert db_doc.path.endswith(doc_name)


def test_import_document():
    """
    Asserts that document import from a flat directory structure works correctly.
    """
    runner = CliRunner()
    result = runner.invoke(cli, ("import", "documents", str(INVOICES_FLAT)))
    assert result.exit_code == 0
    output_string = "Importing documents from kescher/tests/fixtures/invoices_flat..."
    assert output_string in result.output
    assert len(Document.select()) == 12
    for doc_name, doc_hash in DOC_HASHES.items():
        for db_doc in Document.select().where(Document.hash == doc_hash):
            assert db_doc.path.endswith(doc_name)


def test_show_journal_errors():
    """
    Test if the column filter returns only the desired columns (on exact match!).
    """
    # Test with invalid filter character
    runner_char = CliRunner()
    result_char = runner_char.invoke(
        cli, ("show", "journal", "--filter", "sender:Klausi Meyer")
    )
    assert result_char.exit_code == 1
    assert result_char.output.strip() == "Filter must contain exactly one '='"

    # Test with invalid filter character
    runner_col = CliRunner()
    result_col = runner_col.invoke(
        cli, ("show", "journal", "--filter", "send=Klausi Meyer")
    )
    assert result_col.exit_code == 1
    assert result_col.output.strip() == "send is not a filterable column"


def test_show_journal_filtered(journal_filtered_klausi_meyer):
    """
    Test if the column filter returns only the desired columns (on exact match!).
    """
    #
    runner = CliRunner()
    result = runner.invoke(cli, ("show", "journal", "--filter", "sender=Klausi Meyer"))
    assert result.exit_code == 0
    output = result.output.strip().split("\n")
    assert len(journal_filtered_klausi_meyer) == len(output)
    for line in journal_filtered_klausi_meyer:
        assert line in output

    # Check for empty result on non existing sender Klaus (instead of Klausi)
    result = runner.invoke(cli, ("show", "journal", "--filter", "sender=Klaus Meyer"))
    assert result.exit_code == 0
    output = result.output.strip().split("\n")
    assert len(output) == 3
    for line in [0, 1, 4]:
        assert journal_filtered_klausi_meyer[line] in output


def test_auto_vat():
    """
    Asserts the auto-vat command executes without error.
    The results are checked separately with the show_saldo test command.
    """
    runner = CliRunner()
    result = runner.invoke(cli, ("auto-vat", "19", "USt_Einnahmen", "USt_Ausgaben"))
    assert result.exit_code == 0
    result_again = runner.invoke(
        cli, ("auto-vat", "19", "USt_Einnahmen", "USt_Ausgaben")
    )
    assert result_again.exit_code == 0


def test_show_saldo():
    """
    This test show the saldo of the specified account in the specified range of time.
    """
    runner = CliRunner()
    result_in = runner.invoke(
        cli, ("show", "saldo", "USt_Einnahmen", "2020-01-01", "2020-03-31")
    )
    assert result_in.exit_code == 0
    assert result_in.output.strip() == "Saldo is 18.52"
    result_out = runner.invoke(
        cli, ("show", "saldo", "USt_Ausgaben", "2020-01-01", "2020-03-31")
    )
    assert result_out.exit_code == 0
    assert result_out.output.strip() == "Saldo is 29.48"


def test_show_accounts(expected_accounts):
    """
    Asserts the list of accounts matches the expected accounts.
    """
    runner = CliRunner()
    result = runner.invoke(cli, ("show", "accounts"))
    assert result.exit_code == 0
    output = result.output.strip().split("\n")
    for acc in expected_accounts:
        assert acc in output
    assert len(expected_accounts) == len(output)


def test_show_entry(entry_3):
    """
    Asserts, that the filter results matches expectations of content and formatting.
    The called journalentry should be displayed in one table, and below all corresponding
    entries.
    """
    runner = CliRunner()
    result = runner.invoke(cli, ("show", "entry", "003", "--width=40"))
    assert result.exit_code == 0
    output = result.output.strip().split("\n")
    for res, exp in zip(output, entry_3):
        assert res == exp
