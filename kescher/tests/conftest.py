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
    "┃ID │Sender         │Receiver       │Subject                   │Value    │Balance  ┃",
    "┠───┼───────────────┼───────────────┼──────────────────────────┼─────────┼─────────┨",
    "┃001│Klausi Meyer   │kescher e.V.   │Internet Betrag NO REFEREN│    29.00│  2545.10┃",
    "┖───┴───────────────┴───────────────┴──────────────────────────┴─────────┴─────────┚",
)

ENTRY_3 = (
    "\x1b[33mEntry",
    "┎───┬───────────────┬───────────────┬───────┬─────────┬─────────┒",
    "┃ID │Sender         │Receiver       │Subject│Value    │Balance  ┃",
    "┠───┼───────────────┼───────────────┼───────┼─────────┼─────────┨",
    "┃003│kescher e.V.   │Stromomat GmbH │Strom J│   -64.50│  2260.50┃",
    "┖───┴───────────────┴───────────────┴───────┴─────────┴─────────┚",
    "\x1b[33mBookings",
    "┎───┬────────────────────┬─────┬──────────────────────┬─────────┒",
    "┃ID │Account             │Entry│Comment               │Value    ┃",
    "┠───┼────────────────────┼─────┼──────────────────────┼─────────┨",
    "┃003│USt_Ausgaben        │00003│None                  │    10.30┃",
    "┖───┴────────────────────┴─────┴──────────────────────┴─────────┚",
)

ENTRY_3_BOOKED = (
    "\x1b[33mEntry",
    "┎───┬───────────────┬───────────────┬──────────────────────────┬─────────┬─────────┒",
    "┃ID │Sender         │Receiver       │Subject                   │Value    │Balance  ┃",
    "┠───┼───────────────┼───────────────┼──────────────────────────┼─────────┼─────────┨",
    "┃003│kescher e.V.   │Stromomat GmbH │Strom Januar Betrag NO REF│   -64.50│  2260.50┃",
    "┖───┴───────────────┴───────────────┴──────────────────────────┴─────────┴─────────┚",
    "\x1b[33mBookings",
    "┎───┬────────────────────┬─────┬─────────────────────────────────────────┬─────────┒",
    "┃ID │Account             │Entry│Comment                                  │Value    ┃",
    "┠───┼────────────────────┼─────┼─────────────────────────────────────────┼─────────┨",
    "┃003│USt_Ausgaben        │00003│None                                     │    10.30┃",
    "┠───┼────────────────────┼─────┼─────────────────────────────────────────┼─────────┨",
    "┃007│Strom               │00003│None                                     │    54.20┃",
    "┖───┴────────────────────┴─────┴─────────────────────────────────────────┴─────────┚",
)


@pytest.fixture
def expected_accounts():
    return EXPECTED_ACCOUNTS


@pytest.fixture
def journal_filtered_klausi_meyer():
    return KLAUSI_MEYER


@pytest.fixture
def entry_3():
    return ENTRY_3


@pytest.fixture
def entry_3_booked():
    return ENTRY_3_BOOKED
