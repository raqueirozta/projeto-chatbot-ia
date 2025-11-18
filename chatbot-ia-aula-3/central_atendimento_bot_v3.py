import openai
import os
from dotenv import load_dotenv
import json      
import datetime  

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

system_prompt_central_v2 = """
Você é o Assistente Virtual da Empresa Manual de IA para DEVs, a recepcionista inteligente.
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

**3. Continuação da Conversa (APÓS a primeira resposta):**
   - **Leia TODO o histórico da conversa (contexto).**
   - Responda de forma **natural e conversacional**, ajudando o usuário a progredir dentro da intenção detectada.
   
   - Para VENDAS: Após o usuário indicar o produto, faça perguntas para qualificar
     (ex: "Entendido! E qual seria a quantidade?" ou "Para qual tipo de uso você precisa?").
   
   - Para SUPORTE: Após obter o e-mail, peça detalhes do problema
     (ex: "Obrigado! Poderia descrever o erro que está ocorrendo?").
   
   - Para RH: Após saber a área/vaga, peça o CV ou LinkedIn
     (ex: ""Ótimo! Você pode me enviar o link do seu LinkedIn ou seu e-mail para entrarmos em contato?").
   
   - Mantenha o tom amigável e prestativo.
"""

def iniciar_chat():

    contexto = [{'role': 'system', 'content': system_prompt_central_v2}]
    
    print("\n--- Bot de Atendimento v3 (Salvando Leads) ---")
    print("Assistente IA: Olá! Sou o assistente virtual do Manual de IA. Como posso ajudar?")

    while True:
        try:
            entrada_usuario = input("Você: ")
            
            palavras_saida = ["sair", "tchau", "exit", "ok", "obrigado", "pronto", "só isso"]

            if any(palavra in entrada_usuario.lower() for palavra in palavras_saida):
                print("Assistente IA: Entendido! Só um momento enquanto gero o resumo...")

                prompt_extracao = """
                Analise o histórico da conversa e extraia um JSON com:
                1. intencao (VENDAS, SUPORTE, RH)
                2. nome_cliente
                3. email_cliente
                4. contato_ou_link (telefone, linkedin ou link de curriculo, se houver)
                5. resumo_solicitacao
                
                Responda APENAS o JSON. Se uma informação não foi
                coletada, use o valor 'Não mencionado'.
                """
                contexto.append({'role': 'user', 'content': prompt_extracao})

                resposta_json = get_completion_from_messages(
                    contexto, 
                    json_mode=True, 
                    temperature=0
                )

                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                nome_arquivo = f"lead_{timestamp}.json"

                try:
                    with open(nome_arquivo, 'w', encoding='utf-8') as f:
                        f.write(resposta_json)
                    print(f"\n[SISTEMA]: Lead salvo com sucesso em '{nome_arquivo}'!")
                except Exception as e:
                    print(f"\n[SISTEMA]: Erro ao salvar arquivo: {e}")

                break 
            
            contexto.append({'role': 'user', 'content': entrada_usuario})

            resposta_ia = get_completion_from_messages(contexto, temperature=0.7) 

            if resposta_ia:
                print(f"Assistente IA: {resposta_ia}")
                
                contexto.append({'role': 'assistant', 'content': resposta_ia})
            else:
                print("Assistente IA: Desculpe, tive um problema. Tente novamente.")
                contexto.pop()
            
        except KeyboardInterrupt:
            print("\nAssistente IA: Encerrando...")
            break

if __name__ == "__main__":
    iniciar_chat()