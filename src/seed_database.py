
import sqlite3

# Conecta ao banco de dados
connection = sqlite3.connect("database/delivery.db")
connection.execute("PRAGMA foreign_keys = ON")

# Dados fictícios dos clientes
customers = [
    (1, "Ana Silva", "Contagem", "2026-01-10"),
    (2, "Bruno Costa", "Betim", "2026-01-15"),
    (3, "Carla Souza", "Belo Horizonte", "2026-02-01"),
    (4, "Daniel Lima", "Contagem", "2026-02-12"),
    (5, "Eduarda Alves", "Betim", "2026-03-05"),
    (6, "Felipe Santos", "Belo Horizonte", "2026-03-20"),
    (7, "Gabriela Rocha", "Contagem", "2026-04-02"),
    (8, "Henrique Martins", "Betim", "2026-04-18"),
]

# Restaurantes
restaurants = [
    (1, "Burger House", "Contagem", "Hamburgueria"),
    (2, "Pizza Central", "Belo Horizonte", "Pizzaria"),
    (3, "Sabor Brasileiro", "Betim", "Comida brasileira"),
    (4, "Sushi Express", "Belo Horizonte", "Japonesa"),
]

# Produtos
products = [
    (1, 1, "Hamburguer Classico", 25.00),
    (2, 1, "Hamburguer Duplo", 35.00),
    (3, 1, "Batata Frita", 12.00),
    (4, 2, "Pizza Margherita", 42.00),
    (5, 2, "Pizza Calabresa", 45.00),
    (6, 2, "Refrigerante", 8.00),
    (7, 3, "Prato Executivo", 28.00),
    (8, 3, "Feijoada", 38.00),
    (9, 3, "Suco Natural", 9.00),
    (10, 4, "Combo Sushi 20 pecas", 55.00),
    (11, 4, "Temaki", 22.00),
    (12, 4, "Refrigerante", 8.00),
]

# Pedidos realizados em outubro de 2026
orders = [
    (1, 1, "2026-10-01", "delivered"),
    (2, 2, "2026-10-02", "delivered"),
    (3, 3, "2026-10-03", "delivered"),
    (4, 4, "2026-10-04", "cancelled"),
    (5, 5, "2026-10-05", "delivered"),
    (6, 6, "2026-10-07", "delivered"),
    (7, 7, "2026-10-09", "preparing"),
    (8, 8, "2026-10-10", "delivered"),
    (9, 1, "2026-10-12", "delivered"),
    (10, 2, "2026-10-14", "delivered"),
    (11, 3, "2026-10-16", "delivered"),
    (12, 4, "2026-10-18", "delivered"),
    (13, 5, "2026-10-20", "cancelled"),
    (14, 6, "2026-10-22", "delivered"),
    (15, 7, "2026-10-25", "delivered"),
    (16, 8, "2026-10-28", "delivered"),
]

# Itens de cada pedido:
# (id, pedido, produto, quantidade, preço na compra)
order_items = [
    (1, 1, 1, 2, 25.00),
    (2, 1, 3, 1, 12.00),
    (3, 2, 4, 1, 42.00),
    (4, 2, 6, 2, 8.00),
    (5, 3, 7, 2, 28.00),
    (6, 4, 2, 1, 35.00),
    (7, 5, 10, 1, 55.00),
    (8, 5, 11, 2, 22.00),
    (9, 6, 8, 1, 38.00),
    (10, 6, 9, 2, 9.00),
    (11, 7, 5, 1, 45.00),
    (12, 8, 1, 1, 25.00),
    (13, 8, 3, 2, 12.00),
    (14, 9, 2, 2, 35.00),
    (15, 10, 5, 1, 45.00),
    (16, 10, 6, 1, 8.00),
    (17, 11, 7, 1, 28.00),
    (18, 11, 9, 2, 9.00),
    (19, 12, 4, 2, 42.00),
    (20, 13, 10, 1, 55.00),
    (21, 14, 11, 3, 22.00),
    (22, 15, 1, 2, 25.00),
    (23, 15, 3, 1, 12.00),
    (24, 16, 8, 2, 38.00),
]

# Insere os dados no banco
with connection:
    connection.executemany(
        "INSERT INTO customers VALUES (?, ?, ?, ?)", customers
    )

    connection.executemany(
        "INSERT INTO restaurants VALUES (?, ?, ?, ?)", restaurants
    )

    connection.executemany(
        "INSERT INTO products VALUES (?, ?, ?, ?)", products
    )

    connection.executemany(
        "INSERT INTO orders VALUES (?, ?, ?, ?)", orders
    )

    connection.executemany(
        "INSERT INTO order_items VALUES (?, ?, ?, ?, ?)", order_items
    )

connection.close()

print("Dados inseridos com sucesso!")
