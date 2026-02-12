from gaia.agents.base.tools import tool

async def list_tools() -> list[types.tools]:
    return [
        types.Tool(
            name="list_files",
            description="Lista arquivos recursivamente a partir do diretório raiz.",
            inputSchema={
                "type": "object",
                "properties": {"pattern": {"type": "string"}},
                "required": [],
            },
        ),
        types.Tool(
            name="read_file",
            description="Lê o conteúdo de um arquivo (txt, docx, pdf, xlsx, odt, etc.) usando MarkItDown",
            inputSchema={
                "type": "object",
                "properties": {
                    "relpath": {"type": "string"},
                    "max_bytes": {"type": "number"},
                },
                "required": ["relpath"],
            },
        ),
    ]

@tool
async def list_files() -> list[types.TextContent]:
    pattern = (arguments.get("pattern") or "**/*").strip() or "**/*"
    files = [str(p.relative_to(root)) for p in root.glob(pattern) if p.is_file()]
    return [types.TextContent(type="text", text="\n".join(files))]

@tool
async def read_file() -> list[types.TextContent]:
    relpath = arguments["relpath"]
    max_bytes = int(arguments.get("max_bytes") or 2097152)
    p = (root / relpath).resolve()

    if not str(p).startswith(str(root)):
        return [types.TextContent(type="text", text="Path fora do diretório raiz.")]

    if not p.exists():
        return [types.TextContent(type="text", text=f"Arquivo não encontrado: {relpath}")]

    text = _extract_text(p, max_bytes)
    return [types.TextContent(type="text", text=text)]
