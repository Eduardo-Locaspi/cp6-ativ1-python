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
    while True:
        limpar_tela()
        print("Supermercado")
        print()
        print("0 - Sair")
        print("1 - Cadastrar Produto")
        print("2 - Pesquisar Produto")
        print("3 - Listar registros Cliente")
        print("4 - Editar regitros Produto")
        print("5 - Apagar registros Produto ")
        print()

        opcao = input("Escolha_")
        match opcao:
            case "0":
                sair()
                break
            case "1":
                cadastrar()
            case "2":
                pesquisar_produto()
            case "3":
                escolhaSubmenu()
            case "4":
                editar_produto()
            case "5":
                remover_produto()
            case  _:
                print("Opção selecionada não existe...")

        input("Pressione ENTER para continuar...")  

def sair():
    global conexao
    print("Obrigado por utilizar o nosso código")
    conexao = False

def cadastrar():
    try:
        print("----- CADASTRAR PRODUTO -----")
        # Recebe os valores para cadastro
        nome = input("{:.<25}:".format("Digite o nome do produto: ")).strip()
        setor = input("{:.<25}:".format("Digite o setor: ")).strip()
        data_str = input("{:.<25}:".format("Digite a data de vencimento (DD/MM/YYYY): ")).strip()
        preco = float(input("{:.<25}:".format("Digite o preço: ")))
        qt_produto = int(input("{:.<25}:".format("Digite a quatidade: ")))

        validade = datetime.strptime(data_str, "%d/%m/%Y")
        sql = """ INSERT INTO T_PRODUTO (nm_produto, setor_produto, dt_validade,preco_produto,qt_produto)VALUES (:1,:2,:3,:4,:5) """
        inst_cadastro.execute(sql,(nome, setor, validade, preco, qt_produto))
        conn.commit()
        print("##### Produto cadastrado com sucesso! #####")

    except ValueError:
        print("Digite um valor válido!")
    except:
        print("Erro na transação do BD")
    else:
        # Caso haja sucesso na gravação
        print("##### Dados GRAVADOS #####")

def pesquisar_produto():
    pesquisa = input("Produto: ")
    sql = "SELECT * FROM T_PRODUTO WHERE nm_produto = :1"
    listar_dados(sql, pesquisa)

def escolhaSubmenu():
    print("""a - Listar Todos
b - Pesquisar campo (String)
c - Pesquisar campo (numérico)
""")
    
    opcao = input("Escolha:_").lower()
    match opcao:
        case "0":
            ...
        case "a":
            listar_todos()
        case "b":
            listar_string()
        case _:
            print("Valor inválido")

def listar_todos():
    limpar_tela()
    sql = "SELECT * FROM T_PRODUTO"
    listar_dados(sql)

def listar_string():
    limpar_tela()
    valor_consultado = input("Qual o valor a ser consultado?_")
    sql = "SELECT * FROM T_PRODUTO WHERE nm_produto LIKE :1"
    parametro = f"%{valor_consultado}%"
    listar_dados(sql, parametro)

def listar_dados(sql: str, parametro:str = None) -> None:
    lista_produtos = []  # Lista para captura de dados do Banco
    if not parametro:
    # Instrução SQL com base no que foi selecinado na tela de menu
        inst_consulta.execute(sql)
    else:
        inst_consulta.execute(sql,(parametro,))
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
        print("----- PRODUTOS -----")
        print(dados_df)

def editar_produto():
    try:
        id_prod = int(input("Qual id de produto iremos alterar? "))
        campos_validos = ['nm_produto', 'setor_produto', 'dt_vencimento', 'preco_produto', 'peso']

        campo_alterado = input(f"Qual campo deseja alterar ({', '.join(campos_validos)})? ").strip

        if campo_alterado not in campos_validos:
            print("Campo inválido!")
            return
        
        valor_novo = input("Qual é o novo valor? ").strip()

        instrucao_sql = f"UPDATE T_PRODUTO SET :1 = :2 WHERE cod_produto = :3"

        inst_alteracao.execute(instrucao_sql, (campo_alterado, valor_novo, id_prod))
        print("Produto atualizado com sucesso.")

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
