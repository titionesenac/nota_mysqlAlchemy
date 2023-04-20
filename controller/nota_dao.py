import sqlite3
from model.nota import Nota


class DataBase:
    def __init__(self, nome='system.db'):
        self.connection = None
        self.name = nome

    def connect(self):
        self.connection = sqlite3.connect(self.name)

    def close_connection(self):
        try:
            self.connection.close()
        except sqlite3.Error as e:
            print(e)

    def create_table_nota(self):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS NOTA(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            TITULO TEXT,
            TEXTO TEXT,
            DATA_CRIACAO TEXT,
            PRIORIDADE TEXT
            )
            """
        )
        self.close_connection()

    def registrar_nota(self, nota: Nota):
        self.connect()
        cursor = self.connection.cursor()
        campos_nota = ('TITULO', 'DATA_CRIACAO', 'TEXTO', 'PRIORIDADE')
        valores = f"'{nota.titulo}', '{str(nota.data_criacao)}', '{nota.texto}', '{nota.prioridade}'"

        try:
            cursor.execute(f"""INSERT INTO NOTA {campos_nota} VALUES ({valores})""")
            self.connection.commit()
            return 'OK'
        except sqlite3.Error as e:
            return e
        finally:
            self.close_connection()

    def consultar_nota(self, id):
        self.connect()
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""SELECT * FROM NOTA WHERE ID = '{id}'""")
            return cursor.fetchone()
        except sqlite3.Error as e:
            return None
        finally:
            self.close_connection()

    def consultar_todas_notas(self):
        self.connect()
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""SELECT * FROM NOTA""")
            return cursor.fetchall()
        except sqlite3.Error as e:
            return None
        finally:
            self.close_connection()

    def deletar_nota(self, id):
        self.connect()
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""DELETE FROM NOTA WHERE ID = '{id}'""")
            self.connection.commit()
            return 'OK'
        except sqlite3.Error as e:
            print(e)
        finally:
            self.close_connection()

    def atualizar_nota(self, nota: Nota):
        self.connect()
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""UPDATE NOTA SET
                TITULO = '{nota.titulo}',
                TEXTO = '{nota.texto}',
                PRIORIDADE = '{nota.prioridade}'
                WHERE ID = '{nota.id}'""")
            self.connection.commit()
            return 'OK'
        except sqlite3.Error as e:
            return e
        finally:
            self.close_connection()

