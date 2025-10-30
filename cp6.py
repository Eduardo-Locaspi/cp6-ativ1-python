# Eduardo Batista Locaspi - rm561713 - 1tdspi
# Caio Kenzo Tayra - RM562979 - 1tdspi

import os

import oracledb
import pandas as pd
from datetime import datetime

# -------------------------- SUBALGORITIMOS --------------------------
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def menu(): # Menu Inicial
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

    except ValueError:
        print("Digite um valor válido!")
    except:
        print("Erro na transação do BD")
    else:
        # Caso haja sucesso na gravação
        print("##### Dados GRAVADOS #####")



def escolhaSubmenu(): # SubMenu do item 3
    print("""a - Listar Todos
b - Pesquisar campo (String)
c - Pesquisar campo (numérico)
d - Pesquisa Genérica
Gerar arquivo [E]xcel, [C]sv? ou [ENTER] para voltar ao menu
""")
    
    opcao = input("Escolha:_")
    match opcao:
        case "":
            ...
        case "a":
            df, sql = listar_todos()
        case "b":
            df, sql = listar_string()
        case "c":
            df, sql = listar_numerico()
        case "d":
            df, sql = listar_generico()
        case "E":
            gerar_arquivo(".xlsx")
        case "C":
            gerar_arquivo(".csv")
        case _:
            print("Valor inválido")
    exibir_df(df)
    input("Pressione ENTER para continuar...")

    colunas_sql = listar_coluna()
    print(colunas_sql)
    mostrar_colunas_lista(colunas_sql, sql)


# ============================ CONSULTA

def exibir_df(df: pd.DataFrame) -> None:
    print("----------- Produtos -----------")
    print(df)

def pesquisar_produto():
    pesquisa = input("Produto: ")
    sql = "SELECT * FROM T_PRODUTO WHERE nm_produto = :1"
    df = listar_dados(sql, pesquisa)
    return df

#Função que guarda a instrucao sql
def listar_todos() -> None: 
    limpar_tela()
    sql = "SELECT * FROM T_PRODUTO"
    df = listar_dados(sql)
    return df, sql

def listar_string() -> None:
    limpar_tela()
    valor_consultado = input("Qual o valor a ser consultado?_")
    sql = "SELECT * FROM T_PRODUTO WHERE nm_produto LIKE :1"
    parametro = f"%{valor_consultado}%"
    df = listar_dados(sql, parametro)
    
    return df, sql

def listar_numerico() -> None:
    limpar_tela()
    operador_validos = [">", ">=", "<", "<=", "==", "!="]
    try:
        valor = int(input("Preço: "))
        operador = input("filtro (>, >=, <, <=, == ou !=):") 
        if operador not in operador_validos:
            print("Digite um operador válido")
        else:
            sql = f"SELECT * FROM T_PRODUTO WHERE preco_produto {operador} :1"
            df = listar_dados(sql,valor)
            return df, sql
    except ValueError:
        print("Digite um valor válido!")

def listar_coluna():
    colunas_tabela = ["cod_produto", "nm_produto","setor_produto","dt_validade","preco_produto","qt_prduto"]
    col_selecionada = []
    str_colunas = ""

    limpar_tela()
    
    for i, colunas in enumerate(colunas_tabela, start=1):
        print(f"{i}.{colunas}")

    while True:
        try:
            opcao = int(input("Selecione uma das colunas (Digite 0 para parar):"))
            if opcao == 0:
                break
            elif len(col_selecionada) == len(colunas_tabela):
                print("Todas as colunas foram selecionadas")
                break
            elif opcao > len(colunas_tabela):
                print("Digite um número válido")
            else:
                col_selecionada.append(opcao - 1)

        except TypeError:
            print("Digite um número")

    col_selecionada = sorted(col_selecionada)
    for i in col_selecionada:
        if i < len(col_selecionada) - 1:
            str_colunas += (colunas_tabela[i] + ",")
        else:
            str_colunas += colunas_tabela[i]

    return str_colunas

def mostrar_colunas_lista(colunas_sql: str, sql: str) -> None:
    limpar_tela()
    sql_colunas = sql.replace("*", colunas_sql)
    df = listar_dados(sql_colunas)
    print(sql_colunas)
    print(df) # <- ERRO NANI  TO-DO 
    


def listar_generico():
    limpar_tela()
    valor_consultado = input("Qual o valor a ser consultado?_").strip()
    parametro = f"%{valor_consultado}%"
    df = listar_dados_genericos(parametro)
    print(df)

def listar_dados_genericos(parametro: str) -> pd.DataFrame | str:

    colunas = ["cod_produto","nm_produto","setor_produto","dt_validade","preco_produto","qt_produto"]
    lista_produtos_gen = []

    try:
        for col in colunas:
            sql = f"SELECT * FROM T_PRODUTO WHERE {col} LIKE :1"

            inst_consulta.execute(sql,(parametro,))

            data = inst_consulta.fetchall()
            
            for p in data:
                lista_produtos_gen.append(p)  
            
            lista_produtos_gen = sorted(lista_produtos_gen)
        
        dados_df = pd.DataFrame.from_records(
                lista_produtos_gen, columns=['cod_produto', 'nm_produto', 'setor_produto', 'dt_vencimento', 'preco_produto', 'qt_produto'], index='cod_produto')
        
        if dados_df.empty:
            return "Lista vazia"
        else:
            return dados_df
    except:
        print("Erro na transação do BD")

# funcao que lista todos os itens da tabela
def listar_dados(sql: str, parametro:str = None) -> pd.DataFrame | str:  
    lista_produtos = []  # Lista para captura de dados do Banco
    try:
        # Instrução SQL com base no que foi selecinado na tela de menu
        if not parametro:
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
            lista_produtos, columns=['cod_produto', 'nm_produto', 'setor_produto', 'dt_vencimento', 'preco_produto', 'qt_produto'], index='cod_produto')
        
        # Verifica se não há registro através do dataframe
        if dados_df.empty:
            return "Lista vazia"
        else:
            return dados_df
    except ValueError:
        print("Digite um valor válido!")
    except:
        print("Erro na transação do BD")

def gerar_arquivo(extencao: str) -> None:
    nm_arquivo = input("Digite um nome para o arquivo:").strip()
    df = listar_dados("SELECT * FROM T_PRODUTO")
    if extencao == ".xlsx":
        df.to_excel(nm_arquivo + extencao)
    elif extencao == ".csv":
        df.to_csv(nm_arquivo + extencao)
    else:
        print(f"A extensão '{extencao}' não é válida.")
    

def editar_produto() -> None:
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

def remover_produto() -> None:
    limpar_tela()
    try:
        while True:
            print("----- EXCLUIR PRODUTO -----")
            listar_todos()
            nm_prod = input("Digite o nome do produto que deseja remover:")
            confirmacao = input(f"Tem certeza que quer apagar a registro {nm_prod}? (Sim/Não)").strip().lower()
            if confirmacao in ("sim", "s"):
                sql = f"DELETE FROM T_PRODUTO WHERE nm_produto=:1"
                # Executa a instrução e atualiza a tabela
                inst_exclusao.execute(sql, (nm_prod,))
                conn.commit()
                # Exibe mensagem caso haja sucesso
                print("##### PRODUTO APAGADO! #####")
                break
            elif confirmacao in ("não","nao","n"): 
                print("Deleção cancelada!")
                break
            else:
                print("Digite 'Sim' ou 'Não'")
    except:
        print("Erro na transação do BD")

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
