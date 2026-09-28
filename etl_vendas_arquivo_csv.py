
import os
import sys
import logging
from pathlib import Path
from datetime import datetime

import pyodbc
import pandas as pd
from dotenv import load_dotenv


# ==========================================================
# 1. CONFIGURAÇÕES DO PROJETO
# ==========================================================

# Identifica a pasta onde o script está localizado.
PASTA_PROJETO = Path(__file__).resolve().parent

# Carrega as configurações do arquivo .env.
load_dotenv(PASTA_PROJETO / ".env")

# Recupera as configurações do ambiente.
SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
PASTA_DESTINO = os.getenv("PASTA_DESTINO")

# Define a pasta em que os logs serão armazenados.
PASTA_LOG = PASTA_PROJETO / "logs"

# Cria a pasta de logs caso ela ainda não exista.
PASTA_LOG.mkdir(parents=True, exist_ok=True)

# Configura o registro das execuções.
logging.basicConfig(
    filename=PASTA_LOG / "etl_vendas.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)


# ==========================================================
# 2. VALIDAÇÃO DAS CONFIGURAÇÕES
# ==========================================================

def validar_configuracoes():

    # Dicionário com as configurações obrigatórias.
    configuracoes = {
        "SQL_SERVER": SQL_SERVER,
        "SQL_DATABASE": SQL_DATABASE,
        "PASTA_DESTINO": PASTA_DESTINO
    }

    # Verifica se alguma configuração está ausente ou vazia.
    for nome, valor in configuracoes.items():

        if not valor or not valor.strip():
            raise ValueError(
                f"Configuração obrigatória ausente: {nome}"
            )


# ==========================================================
# 3. CONEXÃO COM O SQL SERVER
# ==========================================================

def conectar_banco():

    # Abre uma conexão utilizando autenticação do Windows.
    # O servidor e o banco são obtidos do arquivo .env.
    conexao = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={SQL_SERVER};"
        f"DATABASE={SQL_DATABASE};"
        "Trusted_Connection=yes;",
        timeout=10
    )

    return conexao


# ==========================================================
# 4. EXTRAÇÃO DOS DADOS
# ==========================================================

def tabela_no_banco(conexao):

    cursor = None

    try:

        # Cria o cursor para executar a consulta SQL.
        cursor = conexao.cursor()

        # Consulta os dados da tabela de vendas.
        cursor.execute("""
            SELECT
                id,
                nome,
                qtd_vendas,
                valor_vendas
            FROM tb_vendas
        """)

        # Recupera todos os registros encontrados.
        resultado = cursor.fetchall()

        return resultado

    finally:

        # Fecha o cursor mesmo se a consulta apresentar erro.
        # A conexão permanece aberta para ser fechada no main().
        if cursor is not None:
            cursor.close()


# ==========================================================
# 5. VALIDAÇÃO DOS DADOS
# ==========================================================

def validar_dados(df):

    # Impede a geração de arquivos sem registros.
    if df.empty:
        raise ValueError(
            "A consulta SQL não retornou registros."
        )

    # Define o layout esperado do arquivo.
    colunas_esperadas = [
        "id",
        "nome",
        "qtd_vendas",
        "valor_vendas"
    ]

    # Verifica a existência e a ordem das colunas.
    if list(df.columns) != colunas_esperadas:
        raise ValueError(
            "O layout dos dados está incorreto."
        )

    return True


# ==========================================================
# 6. GERAÇÃO DO ARQUIVO CSV
# ==========================================================

def salvar_arquivo_csv(df, pasta_destino):

    # Obtém a data e o horário da geração.
    data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Monta o nome do arquivo com data e horário.
    nome_arquivo = f"Base_de_Vendas_{data_hora}.csv"

    # Monta o caminho completo do arquivo.
    # Path funciona com caminhos locais e de rede do Windows.
    caminho = Path(pasta_destino) / nome_arquivo

    # Exporta os dados:
    # sep=";"        -> separador ponto e vírgula
    # encoding       -> UTF-8 com BOM, compatível com Excel
    # index=False    -> não exporta o índice do DataFrame
    df.to_csv(
        caminho,
        sep=";",
        encoding="utf-8-sig",
        index=False
    )

    # Retorna o caminho para que o main() possa registrá-lo.
    return caminho


# ==========================================================
# 7. FUNÇÃO PRINCIPAL DO ETL
# ==========================================================

def main():

    # Inicializa a variável para permitir seu uso no finally.
    conexao = None
    status = 0

    logging.info("Iniciando processo ETL de vendas.")

    try:

        # ETAPA 1: valida as configurações do ambiente.
        validar_configuracoes()

        # ETAPA 2: abre a conexão com o SQL Server.
        conexao = conectar_banco()

        logging.info("Conexão SQL Server estabelecida.")

        # ETAPA 3: extrai os registros da tabela de vendas.
        resultado = tabela_no_banco(conexao)

        # Converte os objetos pyodbc.Row em tuplas.
        # Isso garante a interpretação correta pelo pandas.
        resultado = [
            tuple(registro) for registro in resultado
        ]

        # ETAPA 4: transforma os registros em um DataFrame.
        df = pd.DataFrame(
            resultado,
            columns=[
                "id",
                "nome",
                "qtd_vendas",
                "valor_vendas"
            ]
        )

        # ETAPA 5: valida o conteúdo e o layout.
        validar_dados(df)

        logging.info(
            f"Dados validados: {len(df)} registros."
        )

        # ETAPA 6: gera o CSV na pasta configurada.
        arquivo_gerado = salvar_arquivo_csv(
            df,
            PASTA_DESTINO
        )

        # ETAPA 7: registra o resultado da exportação.
        logging.info(
            f"Arquivo gerado: {arquivo_gerado} | "
            f"Registros exportados: {len(df)}"
        )

        print("ETL executado com sucesso!")
        print(f"Arquivo: {arquivo_gerado}")
        print(f"Registros: {len(df)}")

    except Exception:

        # Registra o erro completo, incluindo o traceback.
        logging.exception(
            "Falha durante a execução do ETL."
        )

        print(
            "Processo interrompido. "
            "Consulte o arquivo de log."
        )

        # Código de saída que representa falha.
        status = 1

    finally:

        # Tenta fechar a conexão, caso tenha sido aberta.
        if conexao is not None:

            try:
                conexao.close()

                logging.info(
                    "Conexão SQL Server encerrada."
                )

            except Exception:

                logging.exception(
                    "Erro ao encerrar a conexão SQL Server."
                )

                # Se o encerramento falhar, informa falha
                # ao sistema operacional.
                status = 1

    # Retorna o status somente depois do encerramento.
    return status


# ==========================================================
# 8. INICIALIZAÇÃO DO PROGRAMA
# ==========================================================

if __name__ == "__main__":

    # 0 = sucesso
    # 1 = falha
    sys.exit(main())
