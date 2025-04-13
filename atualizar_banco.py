import sqlite3

# Conectando ao banco de dados (substitua pelo caminho do seu arquivo de banco de dados)
conn = sqlite3.connect('banco_dados.db')
cursor = conn.cursor()  # Criando o cursor

# Dados de exemplo para preenchimento
produtos = [
    ("12345", "Produto Exemplo 1", "Fornecedor X", "UN", 10.0, 15.0, 14.0, 13.0, 100, 10, "Grupo A", "Categoria B", "Marca C", "Subgrupo D", "Ingrediente 1, Ingrediente 2", "Tamanho Médio", "Balanca 1", 5.0, 50.0, "Observação exemplo 1"),
    ("67890", "Produto Exemplo 2", "Fornecedor Y", "KG", 20.0, 30.0, 28.0, 25.0, 50, 5, "Grupo B", "Categoria C", "Marca D", "Subgrupo E", "Ingrediente 3, Ingrediente 4", "Tamanho Grande", "Balanca 2", 10.0, 40.0, "Observação exemplo 2")
]

# Inserindo os dados na tabela produtos usando executemany
cursor.executemany("""
    INSERT INTO produtos (
        codigo, descricao, fornecedor, unidade, preco_compra, preco_venda, preco_prazo, 
        preco_atacado, estoque, estoque_minimo, grupo, categoria, marca, subgrupo, 
        ingredientes, tamanho, balanca, lucro, lucro_porcento, obs
    ) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", produtos)

# Commit para salvar as alterações no banco de dados
conn.commit()

# Fechando a conexão
conn.close()

print("Dados inseridos com sucesso!")
