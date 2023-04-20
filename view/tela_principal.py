from PySide6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, \
    QSizePolicy, QTableWidget, QAbstractItemView, QTableWidgetItem, QTextEdit, QComboBox
from PySide6.QtGui import QBrush, QColor, QFont
from model.nota import Nota
from controller.nota_dao import DataBase
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Bloco de Notas')
        self.setMinimumSize(520, 500)

        self.lbl_id = QLabel('ID')
        self.txt_id = QLineEdit()
        self.lbl_titulo = QLabel('Título da Nota')
        self.txt_titulo = QLineEdit()
        self.lbl_prioridade = QLabel('Prioridade')
        self.cb_prioridade = QComboBox()
        self.cb_prioridade.addItems(['Baixa', 'Média', 'Alta'])
        self.lbl_texto = QLabel('Nota')
        self.txt_texto = QTextEdit()
        self.btn_salvar = QPushButton('Salvar')
        self.btn_limpar = QPushButton('Limpar')
        self.btn_remover = QPushButton('Remover')
        self.tabela_notas = QTableWidget()

        self.tabela_notas.setColumnCount(5)
        self.tabela_notas.setHorizontalHeaderLabels(['Id', 'Título', 'Texto', 'Data da Nota', 'Prioridade'])

        self.tabela_notas.setSelectionMode(QAbstractItemView.NoSelection)
        self.tabela_notas.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_id)
        layout.addWidget(self.txt_id)
        layout.addWidget(self.lbl_titulo)
        layout.addWidget(self.txt_titulo)
        layout.addWidget(self.lbl_prioridade)
        layout.addWidget(self.cb_prioridade)
        layout.addWidget(self.lbl_texto)
        layout.addWidget(self.txt_texto)
        layout.addWidget(self.tabela_notas)
        layout.addWidget(self.btn_salvar)
        layout.addWidget(self.btn_limpar)
        layout.addWidget(self.btn_remover)

        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.container)
        self.container.setLayout(layout)

        self.btn_remover.setVisible(False)
        self.lbl_id.setVisible(False)
        self.txt_id.setVisible(False)
        self.txt_id.setReadOnly(True)
        self.btn_remover.clicked.connect(self.deletar_cliente)
        self.btn_salvar.clicked.connect(self.salvar_nota)
        self.btn_limpar.clicked.connect(self.limpar_campos)

        self.tabela_notas.cellDoubleClicked.connect(self.carrega_dados)
        self.popula_tabela_notas()

    def salvar_nota(self):
        db = DataBase()

        nota = Nota(
            id=self.txt_id.text(),
            titulo=self.txt_titulo.text(),
            data_criacao=datetime.today().strftime('%d/%m/%Y'),
            texto=self.txt_texto.toPlainText(),
            prioridade=self.cb_prioridade.currentText()
        )

        if self.btn_salvar.text() == 'Salvar':
            retorno = db.registrar_nota(nota)
            if retorno == 'OK':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('Cadastro realizado')
                msg.setText('Cadastro realizado com sucesso')
                msg.exec()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Erro ao cadastrar')
                msg.setText(f'Erro ao cadastrar a nota, verifique os dados')
                msg.exec()
        elif self.btn_salvar.text() == 'Atualizar':
            retorno = db.atualizar_nota(nota)

            if retorno == 'OK':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('Atualizar')
                msg.setText('Nota editada com sucesso')
                msg.exec()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Erro ao editar')
                msg.setText(f'Erro ao editar a nota, verifique os dados')
                msg.exec()

        self.limpar_campos()
        self.popula_tabela_notas()

    def deletar_cliente(self):
        db = DataBase()
        retorno = db.deletar_nota(self.txt_id.text())

        if retorno == 'OK':
            msg = QMessageBox()
            msg.setWindowTitle('Remover nota')
            msg.setText(f'A nota de Id {self.txt_id.text()} foi deletada')
            msg.exec()

            self.limpar_campos()
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Remover nota')
            msg.setText('Erro ao remover nota')
            msg.exec()

        self.popula_tabela_notas()

    def limpar_campos(self):
        for widget in self.container.children():
            if isinstance(widget, QLineEdit):
                widget.setText("")
            elif isinstance(widget, QTextEdit):
                widget.setText("")
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)

        self.btn_salvar.setText('Salvar')
        self.btn_remover.setVisible(False)
        self.lbl_id.setVisible(False)
        self.txt_id.setVisible(False)

    def popula_tabela_notas(self):
        self.tabela_notas.setRowCount(0)
        db = DataBase()
        lista_notas = db.consultar_todas_notas()
        self.tabela_notas.setRowCount(len(lista_notas))

        for linha, nota in enumerate(lista_notas):
            cor_nota = ""
            cor_texto = ""
            if (nota[4] == "Baixa"):
                cor_nota = QColor(50, 73, 127)
                cor_texto = QBrush(QColor(255, 255, 255))
            elif (nota[4] == "Média"):
                cor_nota = QColor(223, 213, 165)
                cor_texto = QBrush(QColor(0, 0, 0))
            else:
                cor_nota = QColor(255, 0, 0)
                cor_texto = QBrush(QColor(255, 255, 255))
            for coluna, valor in enumerate(nota):
                item = QTableWidgetItem(str(valor))
                item.setForeground(cor_texto)
                fonte = QFont('Arial', 10)
                fonte.setBold(True)
                item.setFont(fonte)
                self.tabela_notas.setItem(linha, coluna, item)
                self.tabela_notas.item(linha, coluna).setBackground(cor_nota)

    def carrega_dados(self, row):
        self.txt_id.setText(self.tabela_notas.item(row, 0).text())
        self.txt_titulo.setText(self.tabela_notas.item(row, 1).text())
        self.txt_texto.setText(self.tabela_notas.item(row, 2).text())
        prioridade_map = {'Baixa': 0, 'Média': 1, 'Alta': 2}
        self.cb_prioridade.setCurrentIndex(prioridade_map.get(self.tabela_notas.item(row, 4).text(), 0))
        self.btn_salvar.setText('Atualizar')
        self.lbl_id.setVisible(True)
        self.txt_id.setVisible(True)
        self.btn_remover.setVisible(True)
