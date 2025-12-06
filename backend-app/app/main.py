from fastapi import FastAPI
from app.routes import chat

# Cria a aplicação
app = FastAPI()

# Conecta as rotas criadas no outro arquivo
# O prefixo organiza a URL: /api/v1/chat
app.include_router(chat.router, prefix="/api/v1")

# Rota de teste simples
@app.get("/")
async def health():
    return {"status": "API Online 🚀"}