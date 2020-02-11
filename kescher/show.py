from kescher.models import Account, JournalEntry


def show_accounts():
    for account in Account.select():
        yield account


def show_journal(width):
    # subtract width of value and balance from total width
    subject_width = width - 54
    for je in JournalEntry.select():
        yield (
            str(je.id).zfill(3),
            je.sender[:15].ljust(15, "_"),
            je.receiver[:15].ljust(15, "_"),
            je.subject[:subject_width].ljust(subject_width, "_"),
            str(round(je.value, 2)).rjust(9, " "),
            str(round(je.balance, 2)).rjust(9, " "),
        )
