from __future__ import annotations


def dispatch(request_line: str) -> str:
    """
    Pure function: request line -> response line.
    Response format:
      - OK <payload>
      - ERR code=<CODE> msg="<message>"
    """
    line = request_line.strip()
    if not line:
        return 'ERR code=EMPTY msg="empty command"'

    parts = line.split(" ", 1)
    cmd = parts[0].upper()
    rest = parts[1] if len(parts) == 2 else ""

    if cmd == "PING":
        return "OK PONG"

    if cmd == "ECHO":
        # Echo back exact rest (trim only one leading space by split)
        return f"OK {rest}".rstrip()

    if cmd == "HELP":
        return "OK commands=PING,ECHO,HELP,QUIT"

    # QUIT is handled client-side, but if a user sends it to server:
    if cmd == "QUIT":
        return "OK BYE"

    return f'ERR code=UNKNOWN_CMD msg="unknown command: {cmd}"'