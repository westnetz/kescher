from kescher.helpers import Box


def test_box_helper():
    """
    Test the Box class from helpers. This test asserts, that the
    returned rows (top, center, bottom, content) are compliant with
    the specified widths.
    """
    widths = [3, 10, 10, 4]
    content = ["X" * w for w in widths]
    box_helper = Box(widths)
    assert box_helper.top() == "┎───┬──────────┬──────────┬────┒"
    assert box_helper.center() == "┠───┼──────────┼──────────┼────┨"
    assert box_helper.bottom() == "┖───┴──────────┴──────────┴────┚"
    assert box_helper.content(content) == "┃XXX│XXXXXXXXXX│XXXXXXXXXX│XXXX┃"
