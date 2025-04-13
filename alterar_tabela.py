

import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('banco_dados.db')
cursor = conn.cursor()

# Criar a tabela 'vendas' se não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY,
    data DATE,
    hora TIME,
    cliente_id INTEGER,
    total REAL,
    forma_pagamento TEXT,
    observacoes TEXT,
    desconto REAL DEFAULT 0,
    total_com_desconto REAL DEFAULT 0,
    cancelada INTEGER DEFAULT 0
)
""")

# Atualizar o valor da coluna 'cancelada'
cursor.execute("UPDATE vendas SET cancelada = 1 WHERE id = 1")  # Exemplo: alterar o valor para 1 onde id é 1

# Confirmar as alterações
conn.commit()

# Fechar a conexão
conn.close()



