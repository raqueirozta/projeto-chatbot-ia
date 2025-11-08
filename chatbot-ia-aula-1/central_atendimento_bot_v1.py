import openai
import os
from dotenv import load_dotenv

print("Carregando variáveis de ambiente...")
load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print("Setup da API concluído.")

def get_completion_from_messages(
        messages, 
        model="gpt-4o-mini", 
        json_mode=False, 
        temperature=0
        ):
    try:
        request_params = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        if json_mode:
            request_params["response_format"] = {"type": "json_object"}
        response = client.chat.completions.create(**request_params)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Erro ao chamar a API: {e}")
        return None

system_prompt_central_v1 = """
Você é o Assistente Virtual da Empresa Y, a recepcionista inteligente.
Sua função principal é **classificar a intenção** do contato inicial do usuário
e **iniciar a conversa** com a primeira pergunta do script correto.

**1. Analise a Mensagem do Usuário e Classifique a Intenção:**
   - Se parecer interesse em comprar, orçamento, ou info de produtos: 'VENDAS'.
   - Se for reclamação, problema técnico, dúvida pós-venda: 'SUPORTE'.
   - Se for sobre vagas, currículo, trabalhar conosco: 'RH'.
   - Se a intenção não for clara: 'DUVIDA'.

**2. Inicie a Conversa Apropriada (Responda APENAS com UMA destas frases):**
   - Para 'VENDAS': "Olá! Que ótimo seu interesse em nossos produtos/serviços.
     Para direcionar você ao especialista certo, pode me dizer qual produto/serviço mais lhe interessa?"
   
   - Para 'SUPORTE': "Olá! Sinto muito que esteja tendo problemas.
     Para que eu possa registrar seu caso e agilizar o atendimento, qual é o seu e-mail de cadastro conosco?"
   
   - Para 'RH': "Olá! Ficamos felizes com seu interesse em fazer parte da nossa equipe.
     Você poderia, por favor, me informar para qual área ou vaga gostaria de se candidatar?"
   
   - Para 'DUVIDA': "Olá! Obrigado por entrar em contato. Para que eu possa te ajudar melhor,
     você poderia me dizer se seu interesse é sobre nossos produtos (Vendas),
     se precisa de ajuda com algo que já usa (Suporte) ou se é sobre oportunidades de trabalho (RH)?"

**IMPORTANTE:** Responda SOMENTE com a frase inicial apropriada.
"""

def iniciar_chat():
    
    contexto = [{'role': 'system', 'content': system_prompt_central_v1}]
    
    print("\n--- Bot de Atendimento v1 (Sem Memória) ---")
    print("Assistente IA: Olá! Sou o assistente virtual da Empresa Y. Como posso ajudar?")

    while True:
        try:
            entrada_usuario = input("Você: ")
            if entrada_usuario.lower() in ["sair", "tchau", "exit"]:
                print("Assistente IA: Entendido. Tenha um ótimo dia!")
                break

            # Lógica "Sem Memória" (proposital para a Aula 1)
            mensagens_para_api = [
                contexto[0], # O System Prompt
                {'role': 'user', 'content': entrada_usuario}
            ]
            
            resposta_ia = get_completion_from_messages(mensagens_para_api, temperature=0) 

            if resposta_ia:
                print(f"Assistente IA: {resposta_ia}")
            else:
                print("Assistente IA: Desculpe, tive um problema. Tente novamente.")
            
        except KeyboardInterrupt:
            print("\nAssistente IA: Encerrando...")
            break

if __name__ == "__main__":
    iniciar_chat()