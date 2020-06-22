import sys

from kescher.booking import get_account_saldo
from kescher.helpers import Box
from kescher.models import Account


def show_accounts(parent=None, layer=0):
    """
    Show the account tree.
    """
    if not parent:
        accounts = Account.select().where(Account.parent.is_null())
    else:
        accounts = Account.select().where(Account.parent == parent)
    for account in accounts:
        saldo, virtual_saldo = get_account_saldo(account.name, with_virtual=True)
        yield (layer, account.name, saldo, virtual_saldo)
        yield from show_accounts(parent=account, layer=layer + 1)


def show_table(filter_fct, filter_, width):
    """
    Print a table as a table.
    """
    box_helper = None
    try:
        for entry in filter_fct(filter_, width):
            if not box_helper:
                box_helper = Box([len(e) for e in entry])
                print(box_helper.top())
            else:
                print(box_helper.center())
            print(box_helper.content(entry))
        print(box_helper.bottom())

    except ValueError as e:
        sys.exit(e)
