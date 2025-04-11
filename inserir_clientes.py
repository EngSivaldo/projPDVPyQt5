import sqlite3

conn = sqlite3.connect("banco_dados.db")
cursor = conn.cursor()

clientes = [
    ("00001", "Ana Silva", "F", "000.000.001-91", "1234567", "12345-000", "Centro", "1990-01-01", "11 91234-5678", "ana@email.com", "Solteira", "Rua A, 123", "São Paulo", "SP"),
    ("00002", "Bruno Santos", "M", "000.000.002-82", "2345678", "23456-000", "Jardins", "1985-02-15", "21 98765-4321", "bruno@email.com", "Casado", "Av B, 456", "Rio de Janeiro", "RJ"),
    ("00003", "Carla Pereira", "F", "000.000.003-73", "3456789", "34567-000", "Bela Vista", "1992-03-20", "31 99887-6655", "carla@email.com", "Solteira", "Rua C, 789", "Belo Horizonte", "MG"),
]

for codigo, nome, sexo, cpf, rg, cep, bairro, data_nascimento, celular, email, estado_civil, endereco, cidade, uf in clientes:
    cursor.execute("""
        INSERT INTO clientes (
            codigo, nome, sexo, cpf, rg, cep, bairro, data_nascimento,
            celular, email, estado_civil, endereco, cidade, uf
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        codigo, nome, sexo, cpf, rg, cep, bairro, data_nascimento,
        celular, email, estado_civil, endereco, cidade, uf
    ))

conn.commit()
conn.close()

print("Clientes inseridos com sucesso!")
