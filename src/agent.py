
import os
import json
from google import genai
from src.database_tool import run_sql_query


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Chave da API Gemini não encontrada.")

client = genai.Client(api_key=api_key)


sql_tool = {
    "type": "function",
    "name": "run_sql_query",
    "description": (
        "Executa consultas SQL somente para leitura "
        "no banco de dados de uma empresa de delivery."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Consulta SQL que será executada."
            }
        },
        "required": ["query"]
    }
}


database_schema = """
Tabelas disponíveis:

customers:
customer_id, customer_name, city, registration_date

restaurants:
restaurant_id, restaurant_name, city, category

products:
product_id, restaurant_id, product_name, price

orders:
order_id, customer_id, order_date, status

order_items:
order_item_id, order_id, product_id, quantity, unit_price
"""


def ask_agent(question):

    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=f"""
        Você é um analista de dados de uma empresa de delivery.

        Sua tarefa é responder perguntas utilizando consultas SQL.

        Estrutura do banco:
        {database_schema}

        Regras:
        - Utilize somente as tabelas e colunas informadas.
        - Gere somente consultas de leitura (SELECT).
        - Não invente informações.
        - Utilize a ferramenta SQL quando a pergunta exigir dados do banco.
        - Para análises de faturamento, considere somente pedidos
          com status 'delivered'.
        - Explique os resultados em português.

        Pergunta do usuário: {question}
        """,
        tools=[sql_tool]
    )

    for step in interaction.steps:

        if step.type == "function_call" and step.name == "run_sql_query":

            query = step.arguments["query"]

            result = run_sql_query(query)

            final_interaction = client.interactions.create(
                model="gemini-3.5-flash-lite",
                previous_interaction_id=interaction.id,
                input=[
                    {
                        "type": "function_result",
                        "name": step.name,
                        "call_id": step.id,
                        "result": [
                            {
                                "type": "text",
                                "text": json.dumps(
                                    result,
                                    ensure_ascii=False
                                )
                            }
                        ]
                    }
                ]
            )

            return {
                "sql": query,
                "result": result,
                "answer": final_interaction.output_text
            }

    return {
        "sql": None,
        "result": None,
        "answer": interaction.output_text
    }
