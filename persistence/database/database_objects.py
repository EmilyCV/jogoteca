

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Jogo(Base):
    __tablename__ = 'jogo'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    console = Column(String, nullable=False)

    def __init__(self, id=int, nome=str, categoria=str, console=str):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.console = console


class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True, nullable=False)
    nome = Column(String, nullable=False)
    senha = Column(String, nullable=False)

    def __init__(self, id=int, nome=str, senha=str):
        self.id = id
        self.nome = nome
        self.senha = senha

# import sqlite3

# conn = sqlite3.connect('jogoteca.db', check_same_thread=False)

# cursor = conn.cursor()

# cursor.execute(
#     '''
#         CREATE TABLE jogo (
#             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#             nome VARCHAR(50) NOT NULL,
#             categoria VARCHAR(40) NOT NULL,
#             console VARCHAR(20) NOT NULL
#         );
#         CREATE TABLE usuario (
#             id VARCHAR(8) NOT NULL PRIMARY KEY,
#             nome VARCHAR(20) NOT NULL,
#             senha VARCHAR(8) NOT NULL
#         );
#     '''
# )

# print('Tabela criada com sucesso.')

# cursor.executemany(
#     'INSERT INTO usuario (id, nome, senha) VALUES (?, ?, ?)',
#     [
#         ('carlos', 'Carlos Borges', '1234'),
#         ('user2', 'Usuário 2', '1221'),
#         ('user3', 'Usuário 3', '3113')
#     ])

# cursor.execute('select * from usuario')
# print(' -------------  Usuários:  -------------')
# for user in cursor.fetchall():
#     print(user[1])

# cursor.executemany(
#     'INSERT INTO jogo (nome, categoria, console) VALUES (?, ?, ?)',
#     [
#         ('God of War 4', 'Ação', 'PS4'),
#         ('NBA 2k18', 'Esporte', 'Xbox One'),
#         ('Rayman Legends', 'Indie', 'PS4'),
#         ('Super Mario RPG', 'RPG', 'SNES'),
#         ('Super Mario Kart', 'Corrida', 'SNES'),
#         ('Fire Emblem Echoes', 'Estratégia', '3DS'),
#     ])

# cursor.execute('select * from jogo')
# print(' -------------  Jogos:  -------------')
# for jogo in cursor.fetchall():
#     print(jogo[1])

# print('Dados inseridos com sucesso.')

# # commitando senão nada tem efeito
# conn.commit()

# conn.close()
