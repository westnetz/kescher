from decimal import Decimal
from kescher.models import Booking, JournalEntry, VirtualBooking

MIN_WIDTH = 61


class ModelFilter:

    columns = None
    model = None

    def __call__(self, filter_, width, header=True):
        column = None
        if filter_:
            filter_split = filter_.split("=")
            if len(filter_split) != 2:
                raise ValueError("Filter must contain exactly one '='")
            column, filter_string = filter_split
            if not hasattr(self.model, column):
                raise ValueError(f"{column} is not a filterable column")

        if column:
            selector = self.model.select().where(
                getattr(self.model, column) == filter_string
            )
        else:
            selector = self.model.select()

        if header:
            yield [c[3].ljust(c[1]) for c in self.columns]

        for je in selector:
            line = []
            for col, length, just, name in self.columns:
                value = getattr(je, col)
                if isinstance(value, Decimal):
                    value = round(value, 2)
                element = str(value)[:length]
                just_method = getattr(element, just)
                line.append(just_method(length))
            yield line


class JournalFilter(ModelFilter):

    model = JournalEntry
    columns = (
        ["id", 3, "zfill", "ID"],
        ["sender", 15, "ljust", "Sender"],
        ["receiver", 15, "ljust", "Receiver"],
        ["subject", 36, "ljust", "Subject"],
        ["value", 9, "rjust", "Value"],
        ["balance", 9, "rjust", "Balance"],
    )

    def __call__(self, filter_, width, header=True):
        if width <= MIN_WIDTH:
            width = MIN_WIDTH
        self.columns[3][1] = width - 54
        yield from super().__call__(filter_, width, header)


class BookingFilter(ModelFilter):

    model = Booking
    columns = (
        ["id", 3, "zfill", "ID"],
        ["account", 20, "ljust", "Account"],
        ["journalentry_id", 5, "zfill", "Entry"],
        ["comment", 20, "ljust", "Comment"],
        ["value", 9, "rjust", "Value"],
    )

    def __call__(self, filter_, width, header=True):
        if width <= MIN_WIDTH:
            width = MIN_WIDTH
        self.columns[3][1] = width - 39
        yield from super().__call__(filter_, width, header)


class VirtualBookingFilter(ModelFilter):

    model = VirtualBooking
    columns = (
        ["id", 3, "zfill", "ID"],
        ["account", 20, "ljust", "Account"],
        ["comment", 20, "ljust", "Comment"],
        ["value", 9, "rjust", "Value"],
    )

    def __call__(self, filter_, width, header=True):
        if width <= MIN_WIDTH:
            width = MIN_WIDTH
        self.columns[2][1] = width - 33
        yield from super().__call__(filter_, width, header)
