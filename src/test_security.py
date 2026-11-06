
from src.database_tool import run_sql_query


tests = [
    (
        "SELECT permitido",
        "SELECT COUNT(*) AS total FROM orders",
        True
    ),
    (
        "DELETE bloqueado",
        "DELETE FROM orders",
        False
    ),
    (
        "UPDATE bloqueado",
        "UPDATE orders SET status = 'cancelled'",
        False
    ),
    (
        "DROP bloqueado",
        "DROP TABLE orders",
        False
    )
]


print("\nTESTES DE SEGURANÇA DO SQL AGENT\n")

for name, query, should_succeed in tests:

    result = run_sql_query(query)

    succeeded = isinstance(result, list)

    if succeeded == should_succeed:
        print(f"[PASSOU] {name}")
    else:
        print(f"[FALHOU] {name}")
        print(f"Resultado: {result}")


# Verifica se os pedidos continuam intactos
count_result = run_sql_query(
    "SELECT COUNT(*) AS total FROM orders"
)

print("\nVerificação final do banco:")
print(count_result)

if count_result == [{"total": 16}]:
    print("[PASSOU] Os 16 pedidos continuam intactos.")
else:
    print("[ATENÇÃO] A quantidade de pedidos mudou.")
