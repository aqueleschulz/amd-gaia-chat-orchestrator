import logging
import json
from typing import Optional, Dict, Any, List, Union

from gaia.agents.base.agent import Agent
from gaia.llm.lemonade_client import LemonadeClient

from src.nebula.config.settings import settings
from src.nebula.tools.file_tools import list_files, read_file

logger = logging.getLogger("nebula.agent")

class NebulaAgent(Agent):
    def __init__(self, system_prompt: Optional[str] = None):
        default_prompt = (
            "Você é o Nebula, um analista de arquivos experiente.\n"
            "Sua missão é explorar os arquivos na pasta 'data' para responder as perguntas do usuário.\n\n"
            "FERRAMENTAS:\n"
            "- list_files(pattern='*'): Lista nomes de arquivos.\n"
            "- read_file(filename='...'): Lê o conteúdo completo de um arquivo.\n\n"
            "REGRAS DE PENSAMENTO:\n"
            "1. Se você não sabe quais arquivos existem, use 'list_files' primeiro.\n"
            "2. Se você precisa ler um arquivo específico da lista, use 'read_file'.\n"
            "3. Se você já tem a informação para responder, use 'answer'.\n\n"
            "FORMATO OBRIGATÓRIO (JSON):\n"
            "Responda APENAS um JSON válido. Não inclua markdown (```json) ou texto extra.\n\n"
            "Exemplo de Ação:\n"
            "{\"thought\": \"Preciso ver os arquivos.\", \"tool\": \"list_files\", \"tool_args\": {\"pattern\": \"*\"}}\n\n"
            "Exemplo de Resposta Final:\n"
            "{\"thought\": \"Encontrei a informação no arquivo x.\", \"answer\": \"O resultado da análise é...\"}"
        )
        
        self.custom_system_prompt = system_prompt or default_prompt

        super().__init__(
            base_url=settings.lemonade_api_url,
            model_id=settings.model_name,
            debug=True,        
            show_prompts=True
        )
        
        self.tool_map = {
            "list_files": list_files,
            "read_file": read_file
        }
        
        if not hasattr(self, 'llm_client') or self.llm_client is None:
             logger.info("Instanciando LemonadeClient manualmente...")
             self.llm_client = LemonadeClient(base_url=settings.lemonade_api_url, model=settings.model_name)
        
        logger.info(f"NebulaAgent (Custom Loop) inicializado.")

    def _register_tools(self):
        if not hasattr(self, 'tools'): self.tools = []
        self.tools.extend([list_files, read_file])

    async def process_user_query(self, user_input: str) -> str:
        messages = [
            {"role": "system", "content": self.custom_system_prompt},
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

                # Se ela não deu answer, mas pediu tool
                if "tool" in action_data:
                    tool_name = action_data["tool"]
                    
                    if tool_name.lower() == "answer":
                        final_msg = action_data.get("tool_args", {}).get("answer") or action_data.get("answer")
                        return str(final_msg)

                    tool_args = action_data.get("tool_args", {})
                    logger.info(f"🛠️ Executando ferramenta real: {tool_name}")
                    
                    tool_result = self._execute_tool_safe(tool_name, tool_args)
                    
                    observation_msg = {
                        "role": "user", 
                        "content": f"OBSERVAÇÃO DO SISTEMA: O resultado da ferramenta '{tool_name}' foi: {tool_result}. Agora, responda ao usuário usando o campo 'answer' no seu JSON."
                    }
                    messages.append(observation_msg)
                    continue

            except Exception as e:
                logger.error(f"Erro no loop customizado: {e}")
                return f"Erro interno: {str(e)}"

        return "Limite de passos atingido sem resposta conclusiva."

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

    def _execute_tool_safe(self, name: str, args: dict) -> str:
        if name not in self.tool_map:
            return f"Erro: Ferramenta {name} não existe."
        try:
            return str(self.tool_map[name](**args))
        except Exception as e:
            return f"Erro na execução: {e}"

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