"""Miscellaneous helping utilities."""

from datetime import datetime
import sys

def _time() -> str:
    return str(datetime.now().strftime("%Y-%m-%d %H_%M"))

def print_and_exit(text: str, traceback=None, exit_code = -1) -> None:
    print(text)
    if traceback: print("\n" + traceback)
    sys.exit(exit_code)
