# Eduardo Batista Locaspi - rm561713 - 1tdspi
# Caio Kenzo Tayra - RM562979 - 1tdspi

import os 
import oracledb
from datetime import date

import pandas as pd

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def menu():
    limpar_tela()
    print("Supermercado")
    print()
    print("0 - Sair")
    print("1 - Cadastrar Produto")
    print("2 - Pesquisar Produto")
    print("3 - Listar todos os registros Cliente")
 
    opcao()
 
def opcao():
    opcao = input("Escolha_")
    match opcao:
        case "0":
            return 
        case "1":
            cadastrar()
        case "2":
            
            pesquisar()
        case "3":
            ...
            # listar_todos()
        case  _:
            print("Opção selecionada não existe...")
    input("Pressione ENTER para continuar...")  

def cadastrar():
    
    try:
        print("----- CADASTRAR CLIENTE -----")
        # Recebe os valores para cadastro
        nome = input("{:.<25}:".format("NOME "))
        setor = input("{:.<25}:".format("SETOR "))
        categoria = input("{:.<25}:".format("Digite o categoria "))
        preco = float(input("{:.<25}:".format("Digite o preço ")))
        peso = float(input("{:.<25}:".format("Digite o peso ")))
        

        cadastro = f""" INSERT INTO T_PRODUTO (nm_produto, setor_produto, categoria_produto,preco_produto,peso)VALUES ('{nome}', '{setor}', '{categoria}',{preco},{peso}) """

        inst_cadastro.execute(cadastro)
        conn.commit()
    except ValueError:
            
        print("Digite um valor válido!")
    except:
        print("Erro na transação do BD")
    else:
        # Caso haja sucesso na gravação
        print("##### Dados GRAVADOS #####")

def pesquisar():
    print("----- LISTAR PETs -----")
    lista_produtos = []  # Lista para captura de dados do Banco
    pesquisa=input("Produto:_ ")

    # Monta a instrução SQL de seleção de todos os registros da tabela
    inst_consulta.execute(f"SELECT * FROM T_PRODUTO WHERE nome='{pesquisa}'")
    # Captura todos os registros da tabela e armazena no objeto data
    data = inst_consulta.fetchall()

    # Insere os valores da tabela na Lista
    for dt in data:
        lista_dados.append(dt)

    # ordena a lista
    lista_dados = sorted(lista_dados)

    # Gera um DataFrame com os dados da lista utilizando o Pandas
    dados_df = pd.DataFrame.from_records(
        lista_dados, columns=['Id', 'Tipo', 'Nome', 'Idade'], index='Id')

    # Verifica se não há registro através do dataframe
    if dados_df.empty:
        print(f"Não há um Pets cadastrados!")
    else:
        print(dados_df)

#===========================================================

try :
    conn = oracledb.connect(user = "rm561713",password = "290107",dsn = "oracle.fiap.com.br:1521/ORCL")

    inst_cadastro = conn.cursor()
    inst_consulta = conn.cursor()
    inst_alteracao = conn.cursor()
    inst_exclusao= conn.cursor()
except Exception as e:
    print(e)
    conexao=False
else:
    conexao=True


while conexao:
    limpar_tela()

    menu()

    







#==================================================



 

 