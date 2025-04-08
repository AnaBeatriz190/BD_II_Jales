'''Crie um sistema de estoque com para uma classe produto
persistente com atributos: nome, validade e estoque. Implemente
métodos para aumentar/diminuir estoque e checar quais produtos
estão com 8 dias ou menos para vencer.'''

from ZODB import DB
from ZODB.FileStorage import FileStorage
import transaction
from datetime import datetime, timedelta

class Produto:
    def __init__(self, nome, validade, estoque):
        self.nome = nome
        self.validade = validade
        self.estoque = estoque

    def aumentar_estoque(self, quantidade):
        self.estoque += quantidade

    def diminuir_estoque(self, quantidade):
        if quantidade <= self.estoque:
            self.estoque -= quantidade
        else:
            print(f"Estoque insuficiente para {self.nome}")

    def checar_vencimento(self):
        hoje = datetime.now().date()
        return (self.validade - hoje).days <= 8

    def __str__(self):
        return f"{self.nome} - Validade: {self.validade} - Estoque: {self.estoque}"

class Estoque:
    def __init__(self):
        self.produtos = []

    def adicionar_produto(self, nome, validade, estoque):
        for produto in self.produtos:
            if produto.nome == nome:
                produto.aumentar_estoque(estoque)
                return
        novo_produto = Produto(nome, validade, estoque)
        self.produtos.append(novo_produto)

    def listar_produtos_vencendo(self):
        produtos_vencendo = [produto for produto in self.produtos if produto.checar_vencimento()]
        return produtos_vencendo

    def listar_produtos(self):
        return [str(produto) for produto in self.produtos]


storage = FileStorage('estoque.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

if 'estoque' not in root:
    estoque = Estoque()
    root['estoque'] = estoque
else:
    estoque = root['estoque']

estoque.adicionar_produto('Produto A', datetime(2025, 4, 15).date(), 100)
estoque.adicionar_produto('Produto B', datetime(2025, 4, 10).date(), 50)
estoque.adicionar_produto('Produto C', datetime(2025, 4, 20).date(), 200)

print("Produtos no estoque:")
for produto in estoque.listar_produtos():
    print(produto)

print("\nProdutos com 8 dias ou menos para vencer:")
produtos_vencendo = estoque.listar_produtos_vencendo()
for produto in produtos_vencendo:
    print(produto)

estoque.produtos[0].diminuir_estoque(20)

transaction.commit()

connection.close()
db.close()
