'''Crie um Sistema Escolar para registro de frequência dos alunos
nas aulas de cada turma.'''
from ZODB import DB
from ZODB.FileStorage import FileStorage
import transaction
from datetime import datetime

class Aluno:
    def __init__(self, nome, matricula):
        self.nome = nome
        self.matricula = matricula

class Aula:
    def __init__(self, data):
        self.data = data
        self.presencas = {}

    def registrar_presenca(self, aluno, presente):
        self.presencas[aluno.matricula] = presente

class Turma:
    def __init__(self, nome):
        self.nome = nome
        self.alunos = []
        self.aulas = []

    def adicionar_aluno(self, aluno):
        self.alunos.append(aluno)

    def registrar_aula(self, data):
        aula = Aula(data)
        self.aulas.append(aula)
        return aula

storage = FileStorage('escola.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

if 'escola' not in root:
    root['escola'] = {}

escola = root['escola']

turma = Turma('Turma A')
aluno1 = Aluno('Maria Silva', '123')
aluno2 = Aluno('João Oliveira', '456')

turma.adicionar_aluno(aluno1)
turma.adicionar_aluno(aluno2)

aula1 = turma.registrar_aula(datetime(2025, 4, 10))
aula1.registrar_presenca(aluno1, True)  # Maria presente
aula1.registrar_presenca(aluno2, False)  # João ausente

escola['Turma A'] = turma
transaction.commit()

print(f"Frequência na aula de {aula1.data.strftime('%d/%m/%Y')}:")
for aluno in turma.alunos:
    status = "Presente" if aula1.presencas.get(aluno.matricula) else "Ausente"
    print(f"{aluno.nome} - {status}")

connection.close()
db.close()
