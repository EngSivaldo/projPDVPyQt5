import sqlite3

# Conecta ao banco de dados
conn = sqlite3.connect("banco_dados.db")
cursor = conn.cursor()

# Apaga a tabela de clientes (caso queira recomeçar do zero – cuidado!)
# Descomente a linha abaixo se quiser apagar tudo:
cursor.execute("DROP TABLE IF EXISTS clientes")

# Cria a tabela com todas as colunas necessárias
cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT,
        cpf TEXT,
        email TEXT,
        telefone TEXT,
        endereco TEXT,
        nascimento TEXT,
        foto TEXT
    )
""")

conn.commit()
conn.close()

print("✅ Banco de dados atualizado com sucesso!")
