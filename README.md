# Nebula Orchestrator (AMD GAIA Edition)

Em meu último semestre cursando matérias pelo curso de tecnólogo em Análise e Desenvolvimento de Sistemas, escrevi meu Projeto Final, equivalente a um trabalho de conclusão de curso, sobre este projeto de código aberto que utiliza de ferramentas já disponíveis para pequenas e médias empresas utilizarem da inteligência artificial.

### AI Implementation for SMEs / Implementação de IA para PMEs

This repository contains the prototype developed for the final project: **"Artificial Intelligence Implementation into Small Business: A Catalyst For Organizations Without Technological Proficiency"**.

Este repositório contém o protótipo desenvolvido para o trabalho de conclusão de curso: **"Implementação de Inteligência Artificial em Pequenas Empresas: Um Catalisador Para Empresas Sem Expertise Tecnológica"**, escrito por **João Pedro Schulz Rocha**.

---

## 🇺🇸 English Instructions

### Overview
Nebula is an AI Orchestrator designed to run locally using the **AMD GAIA SDK**. It allows Small and Medium Enterprises (SMEs) to interact with their local files (e.g., PDFs, Spreadsheets, Text files) using a natural language chat interface, ensuring data privacy and low latency.

The system uses a **FastAPI** backend to orchestrate an AI Agent (NebulaAgent) that follows a ReAct (Reasoning + Acting) loop to plan and execute tasks.

### Prerequisites
To run this project, you need to set up the following environment:

1.  **Python 3.10+**: Ensure Python is installed and added to your system PATH.
2.  **AMD GAIA SDK**: This project relies on the `amd-gaia` package. Ensure you have access to it or install it via the provided requirements.
3.  **Lemonade Server**: You must have a compatible LLM server (like Lemonade or an OpenAI-compatible endpoint) running locally.
    * *Default URL:* `http://localhost:8000`
4.  **Data Folder**: A local folder named `data/` in the project root containing the files you want the AI to analyze.

### AI Model Setup
You must download an Artificial Intelligence model of your choice (e.g., `DeepSeek-R1-Distill-Llama-8B` or `Gemma-2-9B` in GGUF format).

1.  **Download the model** (via HuggingFace or similar).
2.  **Configure Lemonade Server** to load this model.
3.  **Update Configuration**: Edit the `.env` file (create one based on `.env.example` if needed) or modify `src/nebula/config/settings.py` to match your model name.

### Installation

1.  **Clone this repository:**
    ```bash
    git clone [https://github.com/aqueleschulz/amd-gaia-chat-orchestrator.git](https://github.com/aqueleschulz/amd-gaia-chat-orchestrator.git)
    cd amd-gaia-chat-orchestrator
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # Linux/Mac:
    source .venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Orchestrator:**
    ```bash
    python -m src.nebula.main
    ```

5.  **Access the Application:**
    Open your browser at [http://localhost:5000](http://localhost:5000).

---

## 🇧🇷 Instruções em Português

### Visão Geral
O Nebula é um Orquestrador de IA projetado para rodar localmente usando o **AMD GAIA SDK**. Ele permite que Pequenas e Médias Empresas (PMEs) interajam com seus arquivos locais (ex: PDFs, Planilhas, Textos) usando uma interface de chat em linguagem natural, garantindo privacidade de dados e baixa latência.

O sistema utiliza um backend **FastAPI** para orquestrar um Agente de IA (NebulaAgent) que segue um ciclo ReAct (Raciocínio + Ação) para planejar e executar tarefas.

### Pré-requisitos
Para executar este projeto, é necessário configurar o seguinte ambiente:

1.  **Python 3.10+**: Certifique-se de que o Python esteja instalado e adicionado ao PATH do seu sistema.
2.  **AMD GAIA SDK**: Este projeto depende do pacote `amd-gaia`. Certifique-se de tê-lo instalado via `requirements.txt`.
3.  **Lemonade Server**: Você deve ter um servidor LLM compatível (como Lemonade ou um endpoint compatível com OpenAI) rodando localmente.
    * *URL Padrão:* `http://localhost:8000`
4.  **Pasta de Dados**: Uma pasta local chamada `data/` na raiz do projeto contendo os arquivos que você deseja que a IA analise.

### Configuração do Modelo de IA
É necessário baixar um modelo de Inteligência Artificial de sua escolha (ex: `DeepSeek-R1` ou `Gemma-2` em formato GGUF para execução local).

1.  **Baixe o modelo desejado.**
2.  **Configure o Lemonade Server** para carregar este modelo.
3.  **Atualize a Configuração**: Edite o arquivo `.env` ou modifique `src/nebula/config/settings.py` para corresponder ao nome do modelo carregado.

### Instalação

1.  **Clone este repositório:**
    ```bash
    git clone [https://github.com/aqueleschulz/amd-gaia-chat-orchestrator.git](https://github.com/aqueleschulz/amd-gaia-chat-orchestrator.git)
    cd amd-gaia-chat-orchestrator
    ```

2.  **Crie um Ambiente Virtual (Recomendado):**
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # Linux/Mac:
    source .venv/bin/activate
    ```

3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute o Orquestrador:**
    ```bash
    python -m src.nebula.main
    ```

5.  **Acesse a Aplicação:**
    Abra seu navegador em [http://localhost:5000](http://localhost:5000).

---

### License / Licença
This project is licensed under the MIT License - see the LICENSE file for details.
Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.
