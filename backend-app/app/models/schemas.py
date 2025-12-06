from pydantic import BaseModel

# Define o formato de ENTRADA (O que o usuário manda)
class UserMessage(BaseModel):
    message: str

# Define o formato de SAÍDA (O que a API devolve)
class BotResponse(BaseModel):
    response: str