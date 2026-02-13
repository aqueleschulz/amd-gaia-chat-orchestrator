from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class ToolCallDTO(BaseModel):
    tool: str = Field(..., description="O nome exato da ferramenta a ser chamada (ex: 'list_files').")
    tool_args: Dict[str, Any] = Field(default_factory=dict, description="Os argumentos para a ferramenta.")

class AgentResponseDTO(BaseModel):
    thought: str = Field(..., description="O raciocínio passo-a-passo antes de agir.")
    
    tool_action: Optional[ToolCallDTO] = Field(None, description="Ação de ferramenta, se necessária.")
    
    final_answer: Optional[str] = Field(None, description="A resposta final para o usuário, se não houver mais ferramentas a chamar.")

    @classmethod
    def get_json_schema(cls) -> str:
        return cls.model_json_schema()