import sqlite3

# Cria ou abre o banco
conn = sqlite3.connect("banco_dados.db")
cursor = conn.cursor()

# Exemplo de criação de tabela de clientes
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    cpf_cnpj TEXT,
    sexo TEXT,
    endereco TEXT,
    cidade TEXT,
    uf TEXT,
    cep TEXT,
    rg_ie TEXT,
    celular TEXT,
    telefone TEXT,
    email TEXT,
    data_nascimento TEXT,
    estado_civil TEXT,
    data_cadastro TEXT,
    tipo_cliente TEXT,
    limite_credito REAL,
    limite_disponivel REAL,
    observacao TEXT,
    foto BLOB
)
""")

conn.commit()
conn.close()

print("Banco criado com sucesso.")
