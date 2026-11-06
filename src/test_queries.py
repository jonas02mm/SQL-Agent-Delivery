
import sqlite3

connection = sqlite3.connect("database/delivery.db")

# Consulta 1: quantidade de pedidos por situação
query = """
SELECT
    status,
    COUNT(*) AS total_pedidos
FROM orders
GROUP BY status
ORDER BY total_pedidos DESC;
"""

results = connection.execute(query).fetchall()

print("\n--- PEDIDOS POR STATUS ---")

for row in results:
    print(f"Status: {row[0]} | Pedidos: {row[1]}")


# Consulta 2: faturamento total dos pedidos entregues
query = """
SELECT
    SUM(oi.quantity * oi.unit_price) AS faturamento
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE o.status = 'delivered';
"""

revenue = connection.execute(query).fetchone()[0]

print("\n--- FATURAMENTO ---")
print(f"Faturamento dos pedidos entregues: R$ {revenue:.2f}")


# Consulta 3: cinco produtos com maior faturamento
query = """
SELECT
    p.product_name,
    SUM(oi.quantity) AS quantidade_vendida,
    SUM(oi.quantity * oi.unit_price) AS faturamento
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.status = 'delivered'
GROUP BY p.product_id, p.product_name
ORDER BY faturamento DESC
LIMIT 5;
"""

results = connection.execute(query).fetchall()

print("\n--- TOP 5 PRODUTOS ---")

for row in results:
    print(
        f"Produto: {row[0]} | "
        f"Quantidade: {row[1]} | "
        f"Faturamento: R$ {row[2]:.2f}"
    )

connection.close()
