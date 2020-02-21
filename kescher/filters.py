from decimal import Decimal
from kescher.models import JournalEntry


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
            yield [c[0].ljust(c[1]) for c in self.columns]

        for je in selector:
            line = []
            for col, length, just in self.columns:
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
        ["id", 3, "zfill"],
        ["sender", 15, "ljust"],
        ["receiver", 15, "ljust"],
        ["subject", 36, "ljust"],
        ["value", 9, "rjust"],
        ["balance", 9, "rjust"],
    )

    def __call__(self, filter_, width, header=True):
        JournalFilter.columns[3][1] = width - 54
        yield from super().__call__(filter_, width, header)
