from decimal import Decimal
from kescher.models import Account, JournalEntry


def show_accounts(parent=None, layer=0):
    """
    Show the account tree.
    """
    if not parent:
        accounts = Account.select().where(Account.parent.is_null())
    else:
        accounts = Account.select().where(Account.parent == parent)
    for account in accounts:
        yield "┃ " * layer + f"┣━{account.name}"
        yield from show_accounts(parent=account, layer=layer + 1)


def show_journal(filter_, width, header=True):
    """
    Selects the JournalEntries to be shown and yields them.
    Filters can be given with column:filter_string as the first
    argument. The width is the total width of a row, and therefore
    is responsible for the amount of padding.
    """
    column = None
    subject_width = width - 54
    columns = (
        ("id", 3, "zfill"),
        ("sender", 15, "ljust"),
        ("receiver", 15, "ljust"),
        ("subject", subject_width, "ljust"),
        ("value", 9, "rjust"),
        ("balance", 9, "rjust"),
    )

    if filter_:
        filter_split = filter_.split("=")
        if len(filter_split) != 2:
            raise ValueError("Filter must contain exactly one '='")
        column, filter_string = filter_split
        if not hasattr(JournalEntry, column):
            raise ValueError(f"{column} is not a filterable column")

    if column:
        selector = JournalEntry.select().where(
            getattr(JournalEntry, column) == filter_string
        )
    else:
        selector = JournalEntry.select()

    if header:
        yield [c[0].ljust(c[1]) for c in columns]

    for je in selector:
        line = []
        for col, length, just in columns:
            value = getattr(je, col)
            if isinstance(value, Decimal):
                value = round(value, 2)
            element = str(value)[:length]
            just_method = getattr(element, just)
            line.append(just_method(length))
        yield line
