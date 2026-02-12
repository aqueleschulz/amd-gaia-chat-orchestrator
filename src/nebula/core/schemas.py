from pydantic import BaseModel, Field

class Message(BaseModel):
    role: str
    content: str
    tool_calls: list[ToolCall]

class ToolCall(BaseModel):
    id: str
    type: str = "function"
    function: FunctionResponse

class FunctionResponse(BaseModel):
    name: str
    arguments: str

class ToolRequest(BaseModel):
    type: str
    function: ToolFunction

class ToolFunction(BaseModel):
    name: str
    description: str
    parameters: Parameters

class Parameters(BaseModel):
    type: str
    required: list[str]
    properties: dict[str, Property]

class Property(BaseModel):
    type: str
    description: str

class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: str

class ChatCompletionRequest(BaseModel):
    model: str
    tools: list[ToolRequest]
    messages: list[Message]

class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: list[Choice]


