from __future__ import annotations

import asyncio
from dataclasses import dataclass

from .commands import dispatch
from .protocol import ProtocolError, read_line, write_line


@dataclass(frozen=True)
class ServerConfig:
    host: str = "127.0.0.1"
    port: int = 7070


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    addr = writer.get_extra_info("peername")
    print(f"[server] client connected: {addr}")

    try:
        while True:
            try:
                line = await read_line(reader)
            except ProtocolError as e:
                await write_line(writer, f'ERR code=BAD_REQUEST msg="{e}"')
                break

            if line is None:
                break

            response = dispatch(line)
            await write_line(writer, response)

            # If client asked quit, close connection after responding.
            if line.strip().upper() == "QUIT":
                break

    except Exception as e:
        # Never crash the whole server because one session errored.
        try:
            await write_line(writer, f'ERR code=INTERNAL msg="{type(e).__name__}"')
        except Exception:
            pass
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass
        print(f"[server] client disconnected: {addr}")


async def run_server(cfg: ServerConfig) -> None:
    server = await asyncio.start_server(handle_client, cfg.host, cfg.port)
    addrs = ", ".join(str(sock.getsockname()) for sock in (server.sockets or []))
    print(f"[server] listening on {addrs}")

    async with server:
        await server.serve_forever()