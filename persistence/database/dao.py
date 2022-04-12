from App.models.jogo import Jogo
from App.models.usuario import Usuario
from persistence.database.database import Session

SQL_DELETA_JOGO = "DELETE FROM jogo WHERE id = '{}'"
SQL_JOGO_POR_ID = "SELECT id, nome, categoria, console FROM jogo WHERE id = '{}'"
SQL_USUARIO_POR_ID = "SELECT id, nome, email, senha FROM usuario WHERE id = '{}'"
SQL_ATUALIZA_JOGO = "UPDATE jogo SET nome='{}', categoria='{}', console='{}' WHERE id = '{}'"
SQL_BUSCA_JOGOS = "SELECT * FROM jogo"
SQL_CRIA_JOGO = "INSERT INTO jogo (nome, categoria, console) VALUES ('{}', '{}', '{}')"
SQL_CRIA_USUARIO = "INSERT INTO usuario (id,nome, email, senha) VALUES ('{}','{}', '{}', '{}')"


class JogoDao:
    def __init__(self, db: Session):
        self.__db = db

    def salvar(self, jogo):
        cursor = self.__db()
        if (jogo.id):
            cursor.execute(SQL_ATUALIZA_JOGO.format(jogo.nome,
                           jogo.categoria, jogo.console, jogo.id))
        else:
            cursor.execute(SQL_CRIA_JOGO.format(jogo.nome,
                           jogo.categoria, jogo.console, jogo.id))
        cursor.commit()
        return jogo

    def listar(self):
        cursor = self.__db()
        lista_jogos = cursor.execute(SQL_BUSCA_JOGOS)
        jogos = traduz_jogos(lista_jogos.fetchall())
        return jogos

    def busca_por_id(self, id):
        cursor = self.__db()
        buscar_jogo = cursor.execute(SQL_JOGO_POR_ID.format(id))
        tupla = buscar_jogo.fetchone()
        return Jogo(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def deletar(self, id):
        cursor = self.__db()
        cursor.execute(SQL_DELETA_JOGO.format(id))
        cursor.commit()


class UsuarioDao:
    def __init__(self, db: Session):
        self.__db = db

    def salvar(self, usuario):
        cursor = self.__db()
        cursor.execute(SQL_CRIA_USUARIO.format(usuario.id, usuario.nome,
                                               usuario.email, usuario.senha))
        cursor.commit()
        return usuario

    def buscar_por_id(self, id):
        cursor = self.__db()
        buscar_usuario = cursor.execute(SQL_USUARIO_POR_ID.format(id,))
        dados = buscar_usuario.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario


def traduz_jogos(jogos):
    def cria_jogo_com_tupla(tupla):
        return Jogo(tupla[1], tupla[2], tupla[3], id=tupla[0])
    return list(map(cria_jogo_com_tupla, jogos))


def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2], tupla[3])
