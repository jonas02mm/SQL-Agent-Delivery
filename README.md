# SQL Agent — Delivery

Agente de análise de dados que utiliza Inteligência Artificial para transformar perguntas em linguagem natural em consultas SQL, executá-las em um banco de dados SQLite e apresentar os resultados em português.

O projeto simula um cenário de análise de dados de uma empresa fictícia de delivery.

## Objetivo

Demonstrar, na prática, a aplicação de IA generativa para análise de dados, combinando processamento de linguagem natural, geração de SQL, execução de consultas e interpretação de resultados.

## Funcionalidades

- **Perguntas em linguagem natural:** permite consultar os dados utilizando português.
- **Geração de SQL:** transforma perguntas em consultas SQL automaticamente.
- **Execução de consultas:** acessa o banco SQLite por meio de uma ferramenta integrada ao agente.
- **Interpretação dos resultados:** apresenta respostas em linguagem natural.
- **Interface interativa:** permite conversar com o agente e visualizar as consultas e os dados retornados.
- **Segurança:** restringe o banco a operações de leitura e limita o retorno a 100 registros.
- **Avaliação:** possui testes para verificar a precisão das respostas e o comportamento de segurança.

## Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Desenvolvimento da aplicação |
| SQLite | Armazenamento e consulta dos dados |
| Gemini API | Modelo de IA generativa |
| Google GenAI SDK | Integração com o modelo Gemini |
| Streamlit | Construção da interface |
| SQL | Consultas e análise dos dados |
| Git e GitHub | Versionamento e documentação |

## Arquitetura

O funcionamento do projeto segue este fluxo:

1. O usuário envia uma pergunta pela interface Streamlit.
2. O agente utiliza o Gemini para interpretar a solicitação.
3. Quando necessário, o modelo gera uma consulta SQL e solicita a execução da ferramenta.
4. A ferramenta valida e executa a consulta no SQLite, em modo somente leitura.
5. Os resultados retornam ao modelo.
6. O agente interpreta os dados e apresenta uma resposta em português.

## Estrutura do projeto

```text
SQL-Agent-Delivery/
│
├── app/
│   └── app.py
│
├── database/
│   └── schema.sql
│
├── src/
│   ├── agent.py
│   ├── database_tool.py
│   ├── create_database.py
│   ├── seed_database.py
│   ├── test_queries.py
│   ├── test_gemini.py
│   ├── test_security.py
│   └── evaluate_agent.py
│
├── .gitignore
└── README.md
```

O banco de dados é gerado localmente pelos scripts de criação e preenchimento. Por isso, o arquivo `delivery.db` não é incluído no repositório.

## Banco de dados

Foi desenvolvido um banco relacional com dados fictícios de uma operação de delivery.

As cinco tabelas são:

- `customers`: informações dos clientes.
- `restaurants`: restaurantes cadastrados.
- `products`: produtos e seus respectivos preços.
- `orders`: pedidos e seus status.
- `order_items`: itens, quantidades e preços registrados em cada pedido.

O relacionamento entre pedidos e produtos permite analisar vendas, quantidades comercializadas e faturamento.

Para as análises de faturamento, são considerados somente pedidos com status `delivered`.

## Exemplos de perguntas

- Quantos pedidos existem no banco?
- Quantos restaurantes estão cadastrados?
- Quais foram os cinco produtos com maior faturamento?
- Quais restaurantes possuem maior volume de vendas?

## Segurança e validação

A ferramenta responsável pela execução SQL possui mecanismos de proteção:

- Conexão com o banco em modo somente leitura.
- Bloqueio de operações de alteração ou exclusão de dados.
- Autorização de operações de leitura por meio do mecanismo de autorização do SQLite.
- Limite de 100 registros retornados por consulta.

Foram realizados testes com operações `SELECT`, `DELETE`, `UPDATE` e `DROP`. Todos apresentaram o comportamento esperado, e os 16 pedidos permaneceram intactos.

## Avaliação do agente

Foi desenvolvido um conjunto inicial de cinco perguntas para verificar se o agente consegue recuperar corretamente informações do banco.

**Resultado observado:**

- Testes aprovados: 5 de 5.
- Acurácia no conjunto de testes: 100%.

Esse resultado representa o desempenho apenas nas cinco perguntas avaliadas, não uma garantia de precisão para qualquer solicitação.

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/jonas02mm/SQL-Agent-Delivery.git
cd SQL-Agent-Delivery
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

No Windows, a ativação pode ser feita com:

```powershell
.venv\Scripts\activate
```

### 3. Instalar as dependências

```bash
pip install google-genai streamlit
```

### 4. Configurar a chave da API

Configure a variável de ambiente `GEMINI_API_KEY` com uma chave válida da API Gemini.

Não compartilhe a chave nem a inclua no repositório.

### 5. Criar e preencher o banco

```bash
python -m src.create_database
python -m src.seed_database
```

### 6. Iniciar a aplicação

```bash
streamlit run app/app.py
```

A interface será disponibilizada pelo endereço local informado no terminal.

## Próximas melhorias

- Ampliar o conjunto de testes e avaliar diferentes tipos de perguntas.
- Implementar suporte a múltiplas chamadas de ferramentas pelo agente.
- Aprimorar a validação das consultas SQL.
- Adicionar indicadores e visualizações analíticas.
- Monitorar tempo de resposta e consumo da API.