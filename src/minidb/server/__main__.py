from __future__ import annotations

import argparse
import asyncio

from .main import ServerConfig, run_server


def main() -> None:
    parser = argparse.ArgumentParser(prog="minidb-server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7070)
    args = parser.parse_args()

    cfg = ServerConfig(host=args.host, port=args.port)
    asyncio.run(run_server(cfg))


if __name__ == "__main__":
    main()