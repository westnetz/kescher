import os
import pytest
import kescher.cli as cli
import kescher.importers as importers
import kescher.models as models

from click.testing import CliRunner
from kescher.logging import setup_logging


@pytest.fixture
def initialized_path(tmp_path):
    os.chdir(tmp_path)
    cli.logger = setup_logging(tmp_path)
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["--debug", "init"])
    return tmp_path
