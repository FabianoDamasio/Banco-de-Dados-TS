#pyinstaller --onefile --windowed -i nomedoarquivo.ico nomedoarquivo.py - criar executável
'''
--onefile (uníco arquivo)
--windowed (com janela)
-i nomedoarquivo.ico (ícone do executável)
(colar na pasta dist, as interfaces e o .ico e png)
'''
#importar bibliotecas
import mysql.connector
import pymysql
from PyQt5 import uic,QtWidgets,QtGui
from PyQt5.QtWidgets import *

#criar a conexão com o servidor
conexão = pymysql.connect(
	host = '10.0.0.181',
	user = 'consulta',
	passwd = '123456',
	database = "tsbd"
)

#função limpar no cadastro de alunos
def função_limpar():
	interface.txnomealuno.clear()
	interface.txCPF_CNPJ.clear()
	interface.txendereco.clear()
	interface.txnumero.clear()
	interface.txcomplemento.clear()
	interface.txbairro.clear()
	interface.txcidade.clear()
	interface.txcep.clear()
	interface.comboBoxUF.setCurrentIndex(0)
	interface.comboBoxC.setCurrentIndex(0)
	interface.comboBoxturma.setCurrentIndex(0)

#função limpar na busca
def função_limpar_busca():
	interface.txnomealuno_2.clear()
	interface.txnomealuno_3.clear()
	interface.listWidget.clear()

#função Salvar
def função_salvar():
	if (interface.txnomealuno.text() != ""):
		nome = interface.txnomealuno.text()
		cpfcnpj = interface.txCPF_CNPJ.text()
		endereço = interface.txendereco.text()
		numero = interface.txnumero.text()
		complemento = interface.txcomplemento.text()
		bairro = interface.txbairro.text()
		cidade = interface.txcidade.text()
		cep = interface.txcep.text()
		uf = interface.comboBoxUF.currentText()
		camisa = interface.comboBoxC.currentText()
		turmatx = interface.comboBoxturma.currentText()

		#Gravação na tabela
		cursor = conexão.cursor()
		comando_sql = "INSERT INTO bdalunos (Nome,CPFCNPJ,Edereco,Numero,Complemento,Bairro,Cidade,CEP,Uf,Tcamisa,TTurma) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		dados = (str(nome),str(cpfcnpj),str(endereço),str(numero),str(complemento),str(bairro),str(cidade),str(cep),str(uf),str(camisa),str(turmatx))
		cursor.execute(comando_sql,dados)
		conexão.commit()

		#limpeza dos campos
		interface.txnomealuno.clear()
		interface.txCPF_CNPJ.clear()
		interface.txendereco.clear()
		interface.txnumero.clear()
		interface.txcomplemento.clear()
		interface.txbairro.clear()
		interface.txcidade.clear()
		interface.txcep.clear()
		interface.comboBoxUF.setCurrentIndex(0)
		interface.comboBoxC.setCurrentIndex(0)
		interface.comboBoxturma.setCurrentIndex(0)

	else:
		QMessageBox.warning(None,"Atenção","Dados inválidos")

#Função Turma
def função_salvar_turma():
	turma = interface.txturm.text()
	ano = interface.txnomealuno_5.text()
	dataturma = interface.txnomealuno_6.text()


	#Gravação na tabela
	cursor = conexão.cursor()
	comando_sql = "INSERT INTO turmas (Turma,Ano,Dataturma) VALUES (%s,%s,%s)"
	dados_turma = (str(turma),str(ano),data(dataturma))
	cursor.execute(comando_sql,dados_turma)
	conexão.commit()

	interface.txturm.clear()
	interface.txnomealuno_5.clear()
	interface.txnomealuno_6.clear()


def função_buscar():
	if (interface.txnomealuno_2.text() != "") and (interface.txnomealuno_3.text() == ""):
		buscanome = interface.txnomealuno_2.text()
		
		cursor = conexão.cursor()
		cursor.execute ("SELECT id,Nome,CPFCNPJ,Edereco,Numero,Complemento,Bairro,Cidade,CEP,Uf,Tcamisa,TTurma FROM bdalunos WHERE Nome LIKE '%%%s%%'" % buscanome)
		dadosbuscados = cursor.fetchall()
		cont = len(dadosbuscados)
		for row in dadosbuscados:
			interface.listWidget.addItem(str(row[1]))
		'''linha = (0)
		while cont <= cont:
			for row in dadosbuscados:
			interface.listWidget.insertItem(0, QListWidgetItem (str(row[1])))
			linha = + (1)
			pass'''


		'''for row in dadosbuscados:
			print (row[1])'''

		#Leitura dos dados do banco
		#cursor = conexão.cursor()
		#comando_sql = "SELECT Nome FROM bdalunos"
		#cursor.execute(comando_sql)
		#dados_lidos = cursor.fetchall()
		#print (dados_lidos)



	elif (interface.txnomealuno_3.text() != "") and (interface.txnomealuno_2.text() == ""):
		buscaturma = interface.txnomealuno_3.text()

		cursor = conexão.cursor()
		cursor.execute("SELECT Nome,CPFCNPJ,Edereco,Numero,Complemento,Bairro,Cidade,CEP,Uf,Tcamisa,TTurma FROM bdalunos WHERE TTurma LIKE '%%%s%%'" % buscaturma)
		print (cursor.fetchone())

		#Leitura dos dados do banco
		cursor = conexão.cursor()
		comando_sql = "SELECT Nome FROM bdalunos"
		cursor.execute(comando_sql)
		dados_lidos = cursor.fetchall()

	elif (interface.txnomealuno_2.text() != "") and (interface.txnomealuno_3.text() != ""):
		print("aaaaaa")

	else:
		QMessageBox.information(None,"Atenção","Digite alguma pesquisa")


def função_editar():

	nomelista = interface.listWidget.currentRow()
	nomelistado = interface.listWidget.item(nomelista).text()
	interfacedit.show()


#improtar a interface .ui
app = QtWidgets.QApplication([])
interface = uic.loadUi("interface.ui")
interfacedit = uic.loadUi("interfacedit.ui")
#função de click nos botões
interface.salvar01.clicked.connect(função_salvar)
interface.limpar01.clicked.connect(função_limpar)
interface.btedita.clicked.connect(função_editar)
interface.btpesquisa.clicked.connect(função_buscar)
interface.salvar01_2.clicked.connect(função_salvar_turma)
interface.btlimparbusca.clicked.connect(função_limpar_busca)


#ações enter
interface.txnomealuno_2.returnPressed.connect(função_buscar)
interface.txnomealuno_3.returnPressed.connect(função_buscar)


cursor = conexão.cursor()
cursor.execute("SELECT Turma FROM turmas")
teste1 = cursor.fetchall()
interface.comboBoxturma.addItem(str(teste1))

#executar interface
interface.show()
app.exec()


#criar tabela
'''
CREATE TABLE bdalunos (
    id INT NOT NULL AUTO_INCREMENT,
    Nome CHAR (80),
    CPFCNPJ DOUBLE,
    Edereco CHAR (50),
    Numero INT,
    Complemento DOUBLE,
    Bairro CHAR,
    Cidade CHAR,
    CEP DOUBLE,
    Uf CHAR (2),
    Tcamisa CHAR (2),
    PRIMARY key (id)
);
'''
