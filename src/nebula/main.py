import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from src.nebula.core.agent import NebulaAgent
from src.nebula.config.settings import settings

app = FastAPI(
    title="Nebula Orchestrator API",
    description="API para orquestração de chat com acesso ao sistema de arquivos local.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
try:
    print(f"[Nebula] Inicializando Agente no diretório: {settings.workspace_dir.resolve()}")
    settings.workspace_dir.mkdir(parents=True, exist_ok=True)
    agent = NebulaAgent()
except Exception as e:
    print(f"[Fatal] Erro ao iniciar o Agente: {e}")
    agent = None

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    citations: List[str] = []

@app.get("/health")
async def health_check():
    return {
        "status": "online",
        "model": settings.model_name,
        "agent_ready": agent is not None
    }

@app.post("/api/ask", response_model=ChatResponse)
async def ask_endpoint(request: ChatRequest):
    if not agent:
        raise HTTPException(status_code=503, detail="Agente não inicializado corretamente.")
    
    try:
        response_text = await agent.process_user_query(request.question)
        return ChatResponse(answer=response_text, citations=[])
    except Exception as e:
        print(f"[Erro API] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

frontend_path = Path(__file__).parent.parent.parent / "frontend"

if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="static")
    print(f"[Nebula] Frontend montado em: {frontend_path}")
else:
    print(f"[Aviso] Pasta frontend não encontrada em: {frontend_path}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)