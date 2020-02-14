import csv

from click.testing import CliRunner
from kescher.sanitizers import sanitize_postbank
from pathlib import Path

BASE_PATH = Path("kescher/tests/fixtures/sanitizers")
POSTBANK_STATEMENT = (
    BASE_PATH / "Umsatzauskunft_KtoNr01234567890_03-01-2020_17-18-19.csv"
)
POSTBANK_GOLDEN_MASTER = BASE_PATH / "Umsatzauskunft_sanitized_master.csv"


def test_sanitize_postbank_regular(tmp_path):
    outfilename = tmp_path / "Umsatzauskunft_sanitized.csv"
    runner = CliRunner()
    result = runner.invoke(
        sanitize_postbank, (str(POSTBANK_STATEMENT), str(outfilename))
    )
    assert result.exit_code == 0

    golden_master = []
    sanitized = []
    with open(POSTBANK_GOLDEN_MASTER) as infile:
        golden_master_reader = csv.reader(infile, quotechar='"', delimiter=";")
        for row in golden_master_reader:
            golden_master.append(row)
    with open(outfilename) as outfile:
        sanitized_reader = csv.reader(outfile, quotechar='"', delimiter=";")
        for row in sanitized_reader:
            sanitized.append(row)

    assert len(golden_master) == len(sanitized)

    for l, line in enumerate(golden_master):
        assert line == sanitized[l]
