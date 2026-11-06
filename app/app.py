
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from src.agent import ask_agent
from src.database_tool import run_sql_query


# Configuração da página
st.set_page_config(
    page_title="SQL Agent | Delivery",
    page_icon="📊",
    layout="wide"
)


# Estilo visual
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    [data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.08);
        padding: 16px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


# Cabeçalho
st.title("📊 SQL Agent")
st.caption("Assistente inteligente de análise de dados — Delivery")


# Indicadores do banco
st.subheader("Visão geral do banco de dados")

col1, col2, col3 = st.columns(3)

metrics = [
    ("Pedidos", "SELECT COUNT(*) AS total FROM orders"),
    ("Restaurantes", "SELECT COUNT(*) AS total FROM restaurants"),
    ("Produtos", "SELECT COUNT(*) AS total FROM products")
]

for column, (label, query) in zip(
    [col1, col2, col3],
    metrics
):
    result = run_sql_query(query)

    if isinstance(result, list):
        column.metric(label, result[0]["total"])
    else:
        column.metric(label, "Indisponível")


st.divider()


# Apresentação do assistente
st.subheader("Converse com seus dados")

st.write(
    "Faça perguntas em português sobre pedidos, clientes, "
    "produtos, restaurantes e faturamento."
)


# Histórico da conversa
if "messages" not in st.session_state:
    st.session_state.messages = []


# Botão para limpar conversa
if st.button("Limpar conversa"):
    st.session_state.messages = []
    st.rerun()


# Exibição das mensagens anteriores
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message.get("sql"):
            with st.expander("Visualizar consulta SQL"):
                st.code(message["sql"], language="sql")

        if message.get("result") is not None:
            with st.expander("Visualizar dados retornados"):
                if isinstance(message["result"], list):
                    st.dataframe(
                        message["result"],
                        use_container_width=True
                    )
                else:
                    st.json(message["result"])


# Campo de pergunta
question = st.chat_input(
    "Ex.: Quais foram os produtos com maior faturamento?"
)


if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Analisando os dados..."):

            try:
                response = ask_agent(question)

                answer = response["answer"]
                sql = response["sql"]
                result = response["result"]

                st.markdown(answer)

                if sql:
                    with st.expander("Visualizar consulta SQL"):
                        st.code(sql, language="sql")

                if result is not None:
                    with st.expander("Visualizar dados retornados"):
                        if isinstance(result, list):
                            st.dataframe(
                                result,
                                use_container_width=True
                            )
                        else:
                            st.json(result)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sql": sql,
                    "result": result
                })

            except Exception as error:
                st.error(
                    f"Não foi possível processar sua pergunta: {error}"
                )
