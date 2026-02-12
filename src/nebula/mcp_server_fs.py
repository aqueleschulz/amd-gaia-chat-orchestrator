import asyncio
from pathlib import Path
from typing import Any

import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server

from markitdown import MarkItDown

from .config import DRIVE_ROOT

server = Server("fs-context")

def _extract_text(p: Path, max_bytes: int) -> str:
    try:
        md = MarkItDown()
        result = md.convert(str(p))
        text = result.text_content.strip()
        return text[:max_bytes] if text else "(Arquivo sem conteúdo legível)"
    except Exception as e:
        
        SAFE_TEXT_EXTS = {'.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.log', '.csv'}
        
        if p.suffix.lower() in SAFE_TEXT_EXTS:
            try:
                data = p.read_bytes()[:max_bytes]
                return data.decode("utf-8", errors="ignore")
            except Exception:
                pass
        
        # Retornar o erro da conversão
        return f"(Erro na conversão do arquivo {p.name}: {str(e)})"


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    root = DRIVE_ROOT.resolve()

    list = list_tools()

    if(name is in list)
        name()


async def _run():
    # abrir STDIO como context manager e rodar o servidor
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="fs-context",
                server_version="0.2.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def main():
    asyncio.run(_run())


if __name__ == "__main__":
    main()
