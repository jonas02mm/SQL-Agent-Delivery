
from src.agent import ask_agent


test_cases = [
    {
        "question": "Quantos pedidos existem no banco?",
        "expected": 16
    },
    {
        "question": "Quantos restaurantes existem cadastrados?",
        "expected": 4
    },
    {
        "question": "Quantos produtos existem cadastrados?",
        "expected": 12
    },
    {
        "question": "Quantos clientes existem cadastrados?",
        "expected": 8
    },
    {
        "question": "Quais foram os cinco produtos com maior faturamento?",
        "expected": [
            ("Pizza Margherita", 126.0),
            ("Hamburguer Classico", 125.0),
            ("Feijoada", 114.0),
            ("Temaki", 110.0),
            ("Prato Executivo", 84.0)
        ]
    }
]


approved = 0


print("\nAVALIAÇÃO DO SQL AGENT\n")


for index, test in enumerate(test_cases, start=1):

    print(f"Teste {index}: {test['question']}")

    try:
        response = ask_agent(test["question"])
        actual = response["result"]
        expected = test["expected"]

        if isinstance(expected, int):

            if (
                isinstance(actual, list)
                and len(actual) == 1
                and len(actual[0]) == 1
            ):
                actual_value = next(iter(actual[0].values()))
            else:
                actual_value = None

            passed = actual_value == expected

        else:

            actual_values = [
                (
                    row.get("product_name"),
                    row.get("total_revenue")
                )
                for row in actual
            ] if isinstance(actual, list) else []

            passed = actual_values == expected

        if passed:
            print("[PASSOU] Resultado correto.")
            approved += 1
        else:
            print("[FALHOU] Resultado diferente do esperado.")
            print("Esperado:", expected)
            print("Obtido:", actual)

    except Exception as error:
        print("[ERRO]", error)

    print("-" * 50)


total = len(test_cases)
accuracy = (approved / total) * 100

print("\nRESULTADO DA AVALIAÇÃO")
print(f"Testes aprovados: {approved}/{total}")
print(f"Acurácia: {accuracy:.1f}%")
