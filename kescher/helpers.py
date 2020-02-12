class Box:
    """
    Box drawing helper. has top(), center() and bottom()
    method and returns a string ready to be printed.
    """

    def __init__(self, widths):
        """
        Expects a list with the width of each column
        """
        self.widths = widths
        self.filler = ["─" * w for w in widths]

    def fill(self, left, center, right, filler=None):
        if not filler:
            filler = self.filler
        return left + center.join(filler) + right

    def top(self):
        return self.fill("┎", "┬", "┒")

    def center(self):
        return self.fill("┠", "┼", "┨")

    def bottom(self):
        return self.fill("┖", "┴", "┚")

    def content(self, content):
        return self.fill("┃", "│", "┃", content)
