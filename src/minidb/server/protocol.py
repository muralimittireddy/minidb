from __future__ import annotations

import asyncio


class ProtocolError(Exception):
    pass


async def read_line(reader: asyncio.StreamReader, *, max_bytes: int = 65_536) -> str | None:
    """
    Read one '\n'-terminated UTF-8 line.
    Returns None if the peer closed cleanly (EOF).
    Raises ProtocolError if the line is too long or invalid UTF-8.
    """
    try:
        raw = await reader.readline()
    except Exception as e:
        raise ProtocolError(f"read failed: {e}") from e

    if raw == b"":  # EOF
        return None

    if len(raw) > max_bytes:
        raise ProtocolError(f"line too long: {len(raw)} bytes (max {max_bytes})")

    try:
        line = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as e:
        raise ProtocolError("invalid UTF-8") from e

    # Normalize line endings
    line = line.rstrip("\r\n")
    return line


async def write_line(writer: asyncio.StreamWriter, line: str) -> None:
    """
    Write one UTF-8 line terminated by '\n'.
    """
    data = (line + "\n").encode("utf-8")
    writer.write(data)
    await writer.drain()