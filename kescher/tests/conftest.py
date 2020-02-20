import pytest


EXPECTED_ACCOUNTS = (
    "┣━Debitoren",
    "┃ ┣━1000",
    "┃ ┣━1001",
    "┃ ┣━1002",
    "┣━Umsatzsteuer",
    "┃ ┣━USt_Einnahmen",
    "┃ ┣━USt_Ausgaben",
    "┣━Aufwendungen",
    "┃ ┣━Internet",
    "┃ ┣━Strom",
    "┃ ┣━Miete",
    "┃ ┣━Telefon",
    "┃ ┣━Anschaffungen",
    "┃ ┃ ┣━Kundenhardware",
    "┃ ┃ ┣━Zentralhardware",
    "┃ ┃ ┣━Verbrauchsmaterialien",
    "┣━Erträge",
    "┃ ┣━Internetanschlüsse",
    "┣━1003",
)


KLAUSI_MEYER = (
    "┎───┬───────────────┬───────────────┬──────────────────────────┬─────────┬─────────┒",
    "┃id │sender         │receiver       │subject                   │value    │balance  ┃",
    "┠───┼───────────────┼───────────────┼──────────────────────────┼─────────┼─────────┨",
    "┃001│Klausi Meyer   │kescher e.V.   │Internet Betrag NO REFEREN│    29.00│  2545.10┃",
    "┖───┴───────────────┴───────────────┴──────────────────────────┴─────────┴─────────┚",
)


@pytest.fixture
def expected_accounts():
    return EXPECTED_ACCOUNTS


@pytest.fixture
def journal_filtered_klausi_meyer():
    return KLAUSI_MEYER
