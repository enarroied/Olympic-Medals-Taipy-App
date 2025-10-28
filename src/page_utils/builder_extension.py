from pathlib import Path

import taipy.gui.builder as tgb


def text_from_file(path: str | Path):
    text = read_text_file(path)
    tgb.text(text, mode="md")
    pass


def read_text_file(path: str | Path, encoding: str = "utf-8") -> str:
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
