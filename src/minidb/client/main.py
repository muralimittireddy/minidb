from __future__ import annotations

import asyncio
import sys


async def run_client(host: str = "127.0.0.1", port: int = 7070) -> None:
    reader, writer = await asyncio.open_connection(host, port)
    print(f"[client] connected to {host}:{port}")
    print("[client] type HELP for commands, QUIT to exit")

    try:
        while True:
            # Basic interactive prompt
            cmd = input("minidb> ").strip()
            if not cmd:
                continue

            # client-side quit
            if cmd.upper() == "QUIT":
                writer.write(b"QUIT\n")
                await writer.drain()
                resp = await reader.readline()
                print(resp.decode("utf-8").rstrip("\r\n"))
                break

            writer.write((cmd + "\n").encode("utf-8"))
            await writer.drain()

            resp = await reader.readline()
            if resp == b"":
                print("[client] server closed connection")
                break

            print(resp.decode("utf-8").rstrip("\r\n"))

    except KeyboardInterrupt:
        print("\n[client] bye")
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass


def main() -> None:
    # Tiny arg parsing without extra deps
    host = "127.0.0.1"
    port = 7070
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])

    asyncio.run(run_client(host, port))


if __name__ == "__main__":
    main()