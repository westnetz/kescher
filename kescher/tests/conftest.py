import pytest


EXPECTED_ACCOUNTS = (
    "┣━Debitoren \x1b[32m0.00",
    "┃ ┣━1000 \x1b[31m-240.00",
    "┃ ┣━1001 \x1b[32m0.00",
    "┃ ┣━1002 \x1b[32m0.00",
    "┣━Umsatzsteuer \x1b[32m0.00",
    "┃ ┣━USt_Einnahmen \x1b[32m18.52",
    "┃ ┣━USt_Ausgaben \x1b[32m29.48",
    "┣━Aufwendungen \x1b[32m0.00",
    "┃ ┣━Internet \x1b[32m0.00",
    "┃ ┣━Strom \x1b[32m0.00",
    "┃ ┣━Miete \x1b[32m0.00",
    "┃ ┣━Telefon \x1b[32m0.00",
    "┃ ┣━Anschaffungen \x1b[32m0.00",
    "┃ ┃ ┣━Kundenhardware \x1b[32m0.00",
    "┃ ┃ ┣━Zentralhardware \x1b[32m0.00",
    "┃ ┃ ┣━Verbrauchsmaterialien \x1b[32m0.00",
    "┣━Erträge \x1b[32m0.00",
    "┃ ┣━Internetanschlüsse \x1b[32m0.00",
    "┣━1003 \x1b[31m-576.00",
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
