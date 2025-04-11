import sqlite3

# Conecta ao banco de dados correto
conexao = sqlite3.connect("banco_dados.db")
cursor = conexao.cursor()

# Lista das colunas desejadas conforme a interface
colunas_desejadas = {
    "codigo": "INTEGER",
    "nome": "TEXT",
    "sexo": "TEXT",
    "cpf": "TEXT",
    "rg": "TEXT",
    "cep": "TEXT",
    "bairro": "TEXT",
    "nasc": "TEXT",
    "celular": "TEXT",
    "email": "TEXT",
    "estado_civil": "TEXT",
    "endereco": "TEXT",
    "cidade": "TEXT",
    "uf": "TEXT",
    "telefone": "TEXT",
    "data_cadastro": "TEXT",
    "tipo_cliente": "TEXT",
    "limite": "REAL",
    "disponivel": "REAL",
    "controlar_limite": "TEXT",
    "obs": "TEXT",
    "foto_path": "TEXT"
}

# Verifica colunas existentes na tabela
cursor.execute("PRAGMA table_info(clientes)")
colunas_existentes = [info[1] for info in cursor.fetchall()]

# Adiciona colunas que ainda não existem
for coluna, tipo in colunas_desejadas.items():
    if coluna not in colunas_existentes:
        try:
            cursor.execute(f"ALTER TABLE clientes ADD COLUMN {coluna} {tipo}")
            print(f"✅ Coluna adicionada: {coluna} ({tipo})")
        except Exception as e:
            print(f"❌ Erro ao adicionar coluna '{coluna}': {e}")
    else:
        print(f"✔️ Coluna já existe: {coluna}")

conexao.commit()
conexao.close()
