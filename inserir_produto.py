import sqlite3

conn = sqlite3.connect("banco_dados.db")
cursor = conn.cursor()

produtos = [
    # Alimentos
    ("1001", "Arroz Branco 5kg", "Fornecedor A", "kg", 15.00, 19.90, 21.00, 18.00, 50, 10, "Alimentos", "Grãos", "Tio João", "Branco", "", "5kg", "N", 4.90, 32.67, ""),
    ("1002", "Feijão Carioca 1kg", "Fornecedor A", "kg", 5.50, 7.50, 8.00, 6.90, 80, 15, "Alimentos", "Grãos", "Kicaldo", "Carioca", "", "1kg", "N", 2.00, 36.36, ""),
    ("1003", "Macarrão Penne 500g", "Fornecedor B", "pct", 2.30, 3.90, 4.20, 3.50, 100, 20, "Alimentos", "Massas", "Renata", "Penne", "Trigo", "500g", "N", 1.60, 69.57, ""),
    
    # Bebidas
    ("2001", "Refrigerante Cola 2L", "Fornecedor C", "un", 4.00, 6.50, 7.00, 5.90, 60, 10, "Bebidas", "Refrigerantes", "Coca", "Cola", "", "2L", "N", 2.50, 62.5, ""),
    ("2002", "Suco de Uva Integral 1L", "Fornecedor D", "un", 6.90, 10.90, 12.00, 10.00, 40, 5, "Bebidas", "Sucos", "Aurora", "Integral", "Uva", "1L", "N", 4.00, 57.97, ""),
    
    # Limpeza
    ("3001", "Detergente Neutro 500ml", "Fornecedor E", "un", 1.20, 2.50, 2.80, 2.20, 200, 30, "Limpeza", "Cozinha", "Ypê", "Neutro", "", "500ml", "N", 1.30, 108.3, ""),
    ("3002", "Sabão em Pó 1kg", "Fornecedor E", "kg", 6.00, 8.90, 9.50, 8.00, 90, 15, "Limpeza", "Roupas", "OMO", "Lavagem Perfeita", "", "1kg", "N", 2.90, 48.33, ""),
    
    # Higiene
    ("4001", "Papel Higiênico 12 rolos", "Fornecedor F", "pct", 8.00, 12.00, 13.00, 11.00, 70, 10, "Higiene", "Banheiro", "Neve", "Folha Dupla", "", "12 rolos", "N", 4.00, 50.0, ""),
    ("4002", "Creme Dental 90g", "Fornecedor G", "un", 2.00, 3.50, 4.00, 3.20, 150, 20, "Higiene", "Bucal", "Colgate", "Total 12", "Menta", "90g", "N", 1.50, 75.0, ""),
    
    # Eletrônicos
    ("5001", "Mouse Óptico USB", "Fornecedor H", "un", 12.00, 20.00, 22.00, 18.00, 30, 5, "Eletrônicos", "Acessórios", "Logitech", "USB", "", "-", "N", 8.00, 66.66, ""),
    ("5002", "Teclado Slim USB", "Fornecedor H", "un", 18.00, 29.90, 32.00, 27.00, 25, 5, "Eletrônicos", "Acessórios", "Multilaser", "Slim", "", "-", "N", 11.90, 66.11, "")
]

for p in produtos:
    cursor.execute("""
        INSERT INTO produtos (
            codigo, descricao, fornecedor, unidade, preco_compra, preco_venda,
            preco_prazo, preco_atacado, estoque, estoque_minimo, grupo,
            categoria, marca, subgrupo, ingredientes, tamanho, balanca,
            lucro, lucro_porcento, obs
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, p)

conn.commit()
conn.close()
print("Produtos completos inseridos com sucesso!")
