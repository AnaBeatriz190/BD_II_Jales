'''Crie um Sistema de Loja de Ecommerce com carrinho persistente
que contenha múltiplos ItemCarrinho como objetos persistentes.'''

from ZODB import DB
from ZODB.FileStorage import FileStorage
import transaction

class ItemCarrinho:
    def __init__(self, produto_nome, quantidade, preco):
        self.produto_nome = produto_nome
        self.quantidade = quantidade
        self.preco = preco

    def total(self):
        return self.quantidade * self.preco

    def __str__(self):
        return f"{self.produto_nome} x{self.quantidade} - {self.preco} cada"


class Carrinho:
    def __init__(self):
        self.itens = []

    def adicionar_item(self, produto_nome, quantidade, preco):
        for item in self.itens:
            if item.produto_nome == produto_nome:
                item.quantidade += quantidade
                return
        novo_item = ItemCarrinho(produto_nome, quantidade, preco)
        self.itens.append(novo_item)

    def remover_item(self, produto_nome):
        for item in self.itens:
            if item.produto_nome == produto_nome:
                self.itens.remove(item)
                return

    def calcular_total(self):
        return sum(item.total() for item in self.itens)

    def listar_itens(self):
        return [str(item) for item in self.itens]


storage = FileStorage('ecommerce.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

if 'carrinho' not in root:
    carrinho = Carrinho()
    root['carrinho'] = carrinho
else:
    carrinho = root['carrinho']

carrinho.adicionar_item('Produto A', 2, 50)
carrinho.adicionar_item('Produto B', 1, 30)
carrinho.adicionar_item('Produto A', 1, 50)

print("Itens no carrinho:")
for item in carrinho.listar_itens():
    print(item)
print(f"Total: {carrinho.calcular_total()}")

carrinho.remover_item('Produto B')

transaction.commit()

connection.close()
db.close()

