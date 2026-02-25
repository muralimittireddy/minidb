from minidb.server.commands import dispatch


def test_ping():
    assert dispatch("PING") == "OK PONG"


def test_echo():
    assert dispatch("ECHO hello") == "OK hello"


def test_help():
    assert dispatch("HELP").startswith("OK commands=")


def test_unknown():
    resp = dispatch("FOO")
    assert resp.startswith("ERR code=UNKNOWN_CMD")