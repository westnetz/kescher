from kescher.models import Account, JournalEntry


def show_accounts():
    for account in Account.select():
        yield account


def show_journal(filter_, width):
    """
    Selects the JournalEntries to be shown and yields them.
    Filters can be given with column:filter_string as the first
    argument. The width is the total width of a row, and therefore
    is responsible for the amount of padding.
    """
    column = None
    subject_width = width - 54

    if filter_:
        filter_split = filter_.split(":")
        if len(filter_split) != 2:
            raise ValueError("Filter must contain exactly one :")
        column, filter_string = filter_split
        if not hasattr(JournalEntry, column):
            raise ValueError(f"{column} is not filterable column")

    if column:
        selector = JournalEntry.select().where(
            getattr(JournalEntry, column) == filter_string
        )
    else:
        selector = JournalEntry.select()

    for je in selector:
        yield (
            str(je.id).zfill(3),
            je.sender[:15].ljust(15, "_"),
            je.receiver[:15].ljust(15, "_"),
            je.subject[:subject_width].ljust(subject_width, "_"),
            str(round(je.value, 2)).rjust(9, " "),
            str(round(je.balance, 2)).rjust(9, " "),
        )
