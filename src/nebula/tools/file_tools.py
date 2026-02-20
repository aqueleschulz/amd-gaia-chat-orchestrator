import os
from pathlib import Path
from markitdown import MarkItDown
from src.nebula.config.settings import settings

md = MarkItDown()

def list_files(pattern: str = "**/*") -> str:
    try:
        root = Path(settings.workspace_dir).resolve()
        if not root.exists():
            return "Erro: Diretório de workspace não existe."

        files = [
            str(p.relative_to(root)) 
            for p in root.glob(pattern) 
            if p.is_file() and not p.name.startswith(".")
        ]
        
        if not files:
            return "Nenhum arquivo encontrado."
            
        return "\n".join(files)
    except Exception as e:
        return f"Erro ao listar arquivos: {str(e)}"

def read_file(filename: str) -> str:
    try:
        root = Path(settings.workspace_dir).resolve()
        file_path = (root / filename).resolve()

        if not str(file_path).startswith(str(root)):
            return "Erro: Tentativa de acesso fora do diretório permitido."

        if not file_path.exists():
            return f"Erro: Arquivo não encontrado: {filename}"

        result = md.convert(str(file_path))
        return result.text_content

    except Exception as e:
        return f"Falha ao ler arquivo: {str(e)}"