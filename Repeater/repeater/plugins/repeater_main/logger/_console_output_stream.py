import sys
from enum import StrEnum
from typing import TextIO

class ConsoleOutputStream(StrEnum):
    STDOUT = "stdout"
    STDERR = "stderr"

def get_console_output_stream(stream: ConsoleOutputStream) -> TextIO:
    if stream == ConsoleOutputStream.STDOUT:
        return sys.stdout
    elif stream == ConsoleOutputStream.STDERR:
        return sys.stderr
    else:
        raise ValueError(f"Invalid console output stream: {stream}")
