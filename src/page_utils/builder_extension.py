"""Holds variants of the taipy gui builder visual elements, with different default
values, or with extra functionalities."""

from pathlib import Path

import taipy.gui.builder as tgb


def text_from_file(path: str | Path):
    """Creates a Taipy markdown text element from a file address directly"""
    text = _read_text_file(path)
    tgb.text(text, mode="md")


def drop_down_selector(value, lov, label, on_change=None, multiple=False):
    """Create a selector element with a drod-down default anc class 'fullwidth'
    It accepts "multiple" argument and defaults to False (as original)
    It accepts `on_change` argument, but `None` value raises a waring, so it's not
        passed unless it's a function.
    """
    kwargs = {
        "value": value,
        "lov": lov,
        "dropdown": True,
        "label": label,
        "class_name": "fullwidth",
        "multiple": multiple,
    }
    # If on_change = None, we get a warning:
    if on_change is not None:
        kwargs["on_change"] = on_change
    tgb.selector(**kwargs)


def _read_text_file(path: str | Path, encoding: str = "utf-8") -> str:
    """
    Utility function, reads a text file and returns its contents as a string.

    Args:
        path: Path to the text file (str or pathlib.Path).
        encoding: Encoding to use when reading (default: 'utf-8').

    Returns:
        The file contents as a string.
    """
    file_path = Path(path)
    return file_path.read_text(encoding=encoding)
