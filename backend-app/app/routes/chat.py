from fastapi import APIRouter
from app.models.schemas import UserMessage, BotResponse

# Cria um roteador isolado para o Chat
router = APIRouter()

# Define o método POST e o endereço /chat
@router.post("/chat", response_model=BotResponse)
async def chat(body: UserMessage):
    # Hoje fazemos apenas um ECO (Devolve o que recebeu)
    return {"response": f"Eco: {body.message}"}