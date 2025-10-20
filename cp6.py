# Eduardo Batista Locaspi - rm561713 - 1tdspi
# Caio Kenzo Tayra - RM562979 - 1tdspi

import os 
import oracledb
import pandas as pd
from datetime import datetime

# -------------------------- SUBALGORITIMOS --------------------------
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
    print("4 - Registrar regitro Produto")
    print("5 - Apagar registro Produto ")
    print()
 
    opcao()
 
def opcao():
    opcao = input("Escolha_")
    match opcao:
        case "0":
            global conexao
            conexao = False
        case "1":
            cadastrar()
        case "2":
            pesquisar_produto()
        case "3":
            listar_todos()
        case "4":
            editar_produto()
        case "5":
            remover_produto()
        case  _:
            print("Opção selecionada não existe...")

    input("Pressione ENTER para continuar...")  

def cadastrar():
    try:
        print("----- CADASTRAR PRODUTO -----")
        # Recebe os valores para cadastro
        nome = input("{:.<25}:".format("Digite o nome do produto: "))
        setor = input("{:.<25}:".format("Digite o setor: "))
        data_str = input("{:.<25}:".format("Digite a data de vencimento (DD/MM/YYYY): "))
        preco = float(input("{:.<25}:".format("Digite o preço: ")))
        qt_produto = int(input("{:.<25}:".format("Digite a quatidade: ")))

        validade = datetime.strptime(data_str, "%d/%m/%Y")
        sql = """ INSERT INTO T_PRODUTO (nm_produto, setor_produto, dt_validade,preco_produto,qt_produto)VALUES (:1,:2,:3,:4,:5) """
        inst_cadastro.execute(sql,(nome, setor, validade, preco, qt_produto))
        conn.commit()

    except ValueError:
        print("Digite um valor válido!")
    except:
        print("Erro na transação do BD")
    else:
        # Caso haja sucesso na gravação
        print("##### Dados GRAVADOS #####")

def pesquisar_produto():
    limpar_tela()
    print("----- PESQUISAR PRODUTO -----")
    
    sql = escolher_produto()
    listar_dados(sql)

def escolher_produto():
    pesquisa=input("Produto_ ")
    return f"SELECT * FROM T_PRODUTO WHERE nm_produto='{pesquisa}'"

def listar_todos():
    limpar_tela()
    print("----- PRODUTOS -----")
    sql = "SELECT * FROM T_PRODUTO"
    listar_dados(sql)

def listar_dados(sql: str) -> None:
    lista_produtos = []  # Lista para captura de dados do Banco
    # Instrução SQL com base no que foi selecinado na tela de menu
    inst_consulta.execute(sql)
    # Captura todos os registros da tabela e armazena no objeto data
    data = inst_consulta.fetchall()
    # Insere os valores da tabela na Lista
    for dt in data:
        lista_produtos.append(dt)
    # ordena a lista
    lista_produtos = sorted(lista_produtos)
    # Gera um DataFrame com os dados da lista utilizando o Pandas
    dados_df = pd.DataFrame.from_records(
        lista_produtos, columns=['cod_produto', 'nm_produto', 'setor_produto', 'dt_vencimento', 'preco_produto', 'peso'], index='cod_produto')
    # Verifica se não há registro através do dataframe
    if dados_df.empty:
        print(f"Não há produto cadastrado!")
    else:
        print(dados_df)

def editar_produto():
    try:
        id_prod = int(input("Qual id de produto iremos alterar? "))
        # Escolher qual é o produto a ser alterado
        # Escolher qual é o campo a ser alterado
        campo_alterado= input("Qual é o campo à ser alterado? ")
        #Qual o valor novo
        valor_novo= input("Qual é o novo valor? ")
        instrucao_sql = f"Update T_PRODUTO set {campo_alterado} = '{valor_novo}' WHERE cod_produto = {id_prod} "
        #alterar o campo
        inst_alteracao.execute(instrucao_sql)
    except ValueError:
        print("Digite um valor válido!")
    except:
        print("Erro na transação do BD")

def remover_produto():
    try:
        print("----- EXCLUIR PRODUTO -----")
        nm_prod = input("Digite o nome do produto que deseja remover:")

        sql = f"DELETE FROM T_PRODUTO WHERE nm_produto=:1"
        # Executa a instrução e atualiza a tabela
        inst_exclusao.execute(sql, (nm_prod,))
        conn.commit()
    except:
        print("Erro na transação do BD")
    else:
        # Exibe mensagem caso haja sucesso
        print("##### PRODUTO APAGADO! #####")

# ==================== CONEXÃO ====================

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
    menu()
