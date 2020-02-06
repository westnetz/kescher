import yaml

from click.testing import CliRunner
from kescher.models import Account
from kescher.cli import cli
from pathlib import Path

KESCHER_DB = "kescher.db"
KESCHER_LOG = "kescher.log"

ACCOUNTS_FILE = "kescher/tests/fixtures/accounts.yaml"


def test_init_creates_db_and_log():
    runner = CliRunner()
    result = runner.invoke(cli, ("--debug", "init"))
    assert Path(KESCHER_DB).is_file()
    assert Path(KESCHER_LOG).is_file()


def test_init_debug_writes_to_log():
    runner = CliRunner()
    result = runner.invoke(cli, ("--debug", "init"))
    with open(KESCHER_LOG) as logfile:
        log_content = logfile.read()
        assert "kescher - DEBUG - Debug mode is on" in log_content


def test_import_accounts():
    runner = CliRunner()
    result = runner.invoke(cli, ["import-accounts", ACCOUNTS_FILE])
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
