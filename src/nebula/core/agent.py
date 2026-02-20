import logging
import json
from typing import Optional, Dict, Any, List

from gaia.agents.base.agent import Agent
from gaia.agents.base import MCPAgent
from gaia.llm.lemonade_client import LemonadeClient

from src.nebula.config.settings import settings
from src.nebula.tools.file_tools import list_files, read_file

logger = logging.getLogger("nebula.agent")

class NebulaAgent(MCPAgent, Agent):
    def __init__(self, system_prompt: Optional[str] = None):
        default_prompt = (
            "Você é o Nebula, um analista de arquivos experiente.\n"
            "Sua missão é explorar os arquivos na pasta 'data' para responder as perguntas do usuário.\n"
        )
        
        self.custom_system_prompt = system_prompt or default_prompt

        super().__init__(
            base_url=settings.lemonade_api_url,
            model_id=settings.model_name,
            debug=True,        
            show_prompts=True
        )
        
        if not hasattr(self, 'llm_client') or self.llm_client is None:
             logger.info("Instanciando LemonadeClient manualmente...")
             self.llm_client = LemonadeClient(base_url=settings.lemonade_api_url, model=settings.model_name)
        
        logger.info("NebulaAgent (Multi-Protocolo MCP) inicializado.")

    def _register_tools(self):
        pass

    def get_mcp_tool_definitions(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "list-files",
                "description": "Lista nomes de arquivos no diretório de workspace usando um padrão",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string", 
                            "description": "Padrão de busca (ex: *.txt, **/*)"
                        }
                    }
                }
            },
            {
                "name": "read-file",
                "description": "Lê e converte o conteúdo completo de um arquivo",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string", 
                            "description": "Nome ou caminho relativo do arquivo"
                        }
                    },
                    "required": ["filename"]
                }
            }
        ]

    def execute_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"🛠️ Executando ferramenta MCP: {tool_name}")
        
        if tool_name == "list-files":
            pattern = arguments.get("pattern", "**/*")
            result = list_files(pattern=pattern)
            return {"status": "success", "files": result}
            
        elif tool_name == "read-file":
            filename = arguments.get("filename")
            result = read_file(filename=filename)
            return {"status": "success", "content": result}
            
        else:
            raise ValueError(f"Unknown tool: {tool_name}") 

    def get_mcp_server_info(self) -> Dict[str, Any]:
        return {
            "name": "Nebula MCP Orchestrator",
            "version": "2.0.0",
            "description": "Orquestrador de IA para PMEs"
        }

    async def process_user_query(self, user_input: str) -> str:
        tools_schema = json.dumps(self.get_mcp_tool_definitions(), indent=2, ensure_ascii=False)
        
        dynamic_system_prompt = (
            f"{self.custom_system_prompt}\n\n"
            f"FERRAMENTAS DISPONÍVEIS (Formato MCP):\n{tools_schema}\n\n"
            "RESPONDA SEMPRE EM FORMATO JSON VÁLIDO.\n"
            "Se precisar usar uma ferramenta, retorne:\n"
            '{"tool": "nome-da-ferramenta", "tool_args": {"parametro": "valor"}}\n'
            "Se já tiver a resposta final, retorne:\n"
            '{"answer": "Sua resposta final amigável aqui"}'
        )

        messages = [
            {"role": "system", "content": dynamic_system_prompt},
            {"role": "user", "content": user_input}
        ]

        max_steps = 10
        for step in range(max_steps):
            logger.info(f"🔄 Passo {step+1}: Enviando histórico para o LLM...")
            try:
                content = self._call_llm_safe(messages)
                logger.info(f"IA Responde: {content[:100]}...")
                
                messages.append({"role": "assistant", "content": content})
                action_data = self._parse_json(content)
                
                if not action_data:
                    return content

                if "answer" in action_data:
                    logger.info(f"Resposta final encontrada: {action_data['answer']}")
                    return action_data["answer"]

                if "tool" in action_data:
                    tool_name = action_data["tool"]
                    if tool_name.lower() == "answer":
                        final_msg = action_data.get("tool_args", {}).get("answer") or action_data.get("answer")
                        return str(final_msg)

                    tool_args = action_data.get("tool_args", {})
                    
                    tool_result = self._execute_tool_safe(tool_name, tool_args)
                    
                    observation_msg = {
                        "role": "user", 
                        "content": f"OBSERVAÇÃO: O resultado da ferramenta '{tool_name}' foi: {tool_result}. Analise isso e responda com 'answer' ou chame outra ferramenta."
                    }
                    messages.append(observation_msg)
                    continue

            except Exception as e:
                logger.error(f"Erro no loop customizado: {e}")
                return f"Erro interno: {str(e)}"

        return "Limite de passos atingido sem resposta conclusiva."

    def _execute_tool_safe(self, name: str, args: dict) -> str:
        try:
            result_dict = self.execute_mcp_tool(tool_name=name, arguments=args)
            return json.dumps(result_dict, ensure_ascii=False)
        except ValueError as e:
             return f"Erro de Validação: {str(e)}"
        except Exception as e:
            return f"Erro na execução da ferramenta: {str(e)}"

    def _call_llm_safe(self, messages: List[Dict]) -> str:
        if hasattr(self.llm_client, 'chat'):
            try:
                response = self.llm_client.chat(
                    messages=messages,
                    model=settings.model_name,
                    stream=False
                )
                return str(response)
            except Exception as e:
                logger.warning(f"Falha em .chat(), tentando .chat_completions(). Erro: {e}")

        if hasattr(self.llm_client, 'chat_completions'):
            response = self.llm_client.chat_completions(
                messages=messages,
                model=settings.model_name,
                timeout=60
            )
            if isinstance(response, dict):
                return response['choices'][0]['message']['content']
            return str(response)

        if hasattr(self.llm_client, 'generate'):
            prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
            return str(self.llm_client.generate(prompt=prompt, model=settings.model_name))

        raise AttributeError("Não foi possível encontrar um método de chat compatível no cliente LLM.")

    def _parse_json(self, text: str) -> Optional[Dict]:
        text = text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        try:
            return json.loads(text)
        except:
            return None