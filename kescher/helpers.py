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

    def _fill(self, left, center, right, filler=None):
        """
        Internal function used by top(), center(), bottom()
        and content(). Returns the created divider, top, bottom
        (if no filler is given) or content row (if filler given).
        """
        if not filler:
            filler = self.filler
        return left + center.join(filler) + right

    def top(self):
        """
        Returns the top of a box specified by self.widths
        """
        return self._fill("┎", "┬", "┒")

    def center(self):
        """
        Returns a row divider of a box specified by self.widths
        """
        return self._fill("┠", "┼", "┨")

    def bottom(self):
        """
        Returns the bottom of a box specified by self.widths
        """
        return self._fill("┖", "┴", "┚")

    def content(self, content):
        """
        Accepts a list/tuple with the cells of a row and
        returns it ready to be printed.
        """
        return self._fill("┃", "│", "┃", content)
