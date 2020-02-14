import pytest


EXPECTED_ACCOUNTS = (
    "Debitoren",
    "1000",
    "1001",
    "1002",
    "Umsatzsteuer",
    "USt_Einnahmen",
    "USt_Ausgaben",
    "Aufwendungen",
    "Internet",
    "Strom",
    "Miete",
    "Telefon",
    "Anschaffungen",
    "Kundenhardware",
    "Zentralhardware",
    "Verbrauchsmaterialien",
    "Erträge",
    "Internetanschlüsse",
    "1003",
)

@pytest.fixture
def expected_accounts():
    return EXPECTED_ACCOUNTS
