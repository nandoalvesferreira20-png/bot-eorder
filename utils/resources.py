from pathlib import Path
import sys


def resource_path(relative_path):
    try:
        base_path = Path(sys._MEIPASS)
    except AttributeError:
        base_path = Path(".")

    return base_path / relative_path