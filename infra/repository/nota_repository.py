from infra.configs.connection import DBConnectionHandler
from infra.entities.nota import Nota


class NotaRepository:

    # Método para realizar a consulta de todas as notas
    def select_all(self):
        with DBConnectionHandler() as db:
            data = db.session.query(Nota).all()
            return data

    # Método para inserir nota no banco de dados
    def insert(self, titulo, texto, prioridade, data_criacao):
        with DBConnectionHandler() as db:
            data_insert = Nota(titulo=titulo, texto=texto, prioridade=prioridade,
                               data_criacao=data_criacao)
            db.session.add(data_insert)
            db.session.commit()

    # Método para realizar a remoção de uma nota do banco de dados
    def delete(self, id):
        with DBConnectionHandler() as db:
            db.session.query(Nota).filter(Nota.id == id).delete()
            db.session.commit()

    # Método para atualizar uma nota
    def update(self, id, titulo, texto, prioridade):
        with DBConnectionHandler() as db:
            db.session.query(Nota).filter(Nota.id == id) \
                .update({'titulo': titulo, 'texto': texto,
                         'prioridade': prioridade})
            db.session.commit()
