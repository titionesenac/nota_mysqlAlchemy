from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from infra.configs.base import Base

class DBConnectionHandler:

    def __init__(self):
        #Dados de endereço do banco de dados
        self.__connection_string = 'mysql+pymysql://admin:admin@localhost:3306/notas'
        #Instância do engine(gerenciador do banco)
        self.__engine = self.__create_database_engine()
        #Sessão nula para que possa ser alocada uma nova ao ser instanciado um obj
        self.session = None
        #Validação de existência de banco de dados ao instanciar um obj
        self.__create_database()

    #Método para validação da existencia do banco de dados, caso
    #não exista realiza criação
    def __create_database(self):
        engine = create_engine(self.__connection_string, echo=True)
        try:
            engine.connect()
        except Exception as e:
            if '1049' in str(e):
                engine = create_engine(self.__connection_string.rsplit('/', 1)[0], echo=True)
                conn = engine.connect()
                conn.execute(f'CREATE DATABASE IF NOT EXISTS {self.__connection_string.rsplit("/", 1)[1]}')
                conn.close()
                print('Banco criado')
                self.__create_table()
            else:
                raise e

    def __create_table(self):
        engine = create_engine(self.__connection_string, echo=True)
        Base.metadata.create_all(bind=engine)

        print("Tabela criada com sucesso!")

    #Função para crição da engine sem necessidade de informar dados de endereço do banco
    #e utilização de queryes escritas à mão
    def __create_database_engine(self):
        engine = create_engine(self.__connection_string)
        return engine

    def get_engine(self):
        return self.__engine

    #Funções mágicas que definem qualquer comportamento ao serem geradas instâncias
    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        print('Gerando conexão')
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Fechando conexão')
        self.session.close()

