import pandas as pd
import zipfile
import os
import re
import sqlite3
from sqlalchemy import create_engine, inspect, MetaData, Table, Column, String, Integer, Float, Date, text


engine = create_engine("sqlite:///../test_analytics.db", echo=True)
metadata = MetaData()
metadata.reflect(bind=engine)

# Extract Zip File
# zip_file_path = "../Data/Data.zip"
# with zipfile.ZipFile(zip_file_path, 'r') as zip:
#   zip.extractall("../Data")

# Constants e Outros
folder_escolas  = "../Data/Data/Escolas"
folder_estudantes = "../Data/Data/Perfil dos educandos"
arquivos_escolas_csv = [arquivo for arquivo in os.listdir(folder_escolas) if arquivo.endswith('.csv')]
arquivos_estudantes_csv = [arquivo for arquivo in os.listdir(folder_estudantes) if arquivo.endswith(".csv")]
date_columns1 = ['dt_criacao', 'doc_criacao', 'dom_criacao', 'dt_ini_conv', 'dt_ini_func', 'dt_autoriza', 'dt_extintao', 'database']
date_columns2 = ['database']
file_path = "../Data/Data/Escolas/dicionarioescolas.xlsx"

# Dicionario de Dados Escola
df = pd.read_excel(file_path)
padrao_cols = df["CAMPO"].to_list()
padrao_cols = [x.lower() for x in padrao_cols]
set1 = set(padrao_cols)

# Auxiliar Dados Escola
lista_arquivos_padrao1 = ["escolas-dez-2010.csv", "escolas-dez-2011.csv", "escolas-dez-2012.csv",
                          "escolas-dez-2013.csv", "escolas-dez-2014.csv", "escolas-dez-2015.csv"]

rename_padrao1 = {
      "cd_cie":"codcie",
      "nomes": "nomesc",
      "nomescofi": "nomescof"
      }

rename_padrao2 = {
      "cd_cie":"codcie",
      "doc_criacao": "dom_criacao",
      "dt_extintao": "dt_extincao",
      "ï»¿dre": "dre",
      "nomes": "nomesc",
      "nomescofi": "nomescof",
      "cdist": "coddist",
      "fx_etaria.1": "fx_etaria"
}

def _converter_data(cols, df):
	for coluna in df.columns:
		if coluna in cols:
			df[coluna] = pd.to_datetime(df[coluna], format="%d/%m/%Y", errors='coerce')

def _padronizar_cols_escolas(df, arquivo):

	new_df = df.copy()
	cols_df = new_df.columns
	cols_df = [x.lower() for x in cols_df]
	new_df.columns = cols_df

	if arquivo in lista_arquivos_padrao1:
		print(new_df.columns)
		new_df = new_df.rename(columns=rename_padrao1)
		print(new_df.columns)
		new_df["dt_ini_func"] = None

	if arquivo in ["escolas122018.csv", "escolas122019.csv"]:
		new_df = new_df.rename(columns=rename_padrao2)
		new_df["nomescof"] = None
	
	if arquivo in ["escolas122020.csv", "escolas122021.csv", "escolas122022.csv"]:
		new_df = new_df.rename(columns=rename_padrao2)
		new_df["dt_ini_func"] = None
	
	if arquivo == "escolas122023.csv":
		new_df = new_df.rename(columns=rename_padrao2)
		new_df["dt_ini_func"] = None
		new_df["nomescof"] = None
		new_df["rede"] = None
		
	if arquivo in ["escolasr34.csv", "escolasr34dez2017.csv"]:
		new_df = new_df.rename(columns=rename_padrao2)
		new_df["dt_extincao"] = None
		new_df["dt_ini_conv"] = None
		new_df["fx_etaria"] = None
		new_df["nomescof"] = None
	
	new_df = new_df[padrao_cols]

	return new_df

def _detect_column_types(df):
    """Detectar os tipos de dados das colunas de um DataFrame."""
    tipos_de_dados = {}
    for coluna in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[coluna]):
            tipos_de_dados[coluna] = Date
        elif pd.api.types.is_integer_dtype(df[coluna]):
            tipos_de_dados[coluna] = Integer
        elif pd.api.types.is_float_dtype(df[coluna]):
            tipos_de_dados[coluna] = Float
        else:
            tipos_de_dados[coluna] = String
    return tipos_de_dados

def carregar_dados_banco(arquivos_csv, folder_path, date_columns, dataset='escola'):

	i = 0
	for arquivo in arquivos_csv:
		print(arquivo)
		print(f"Iteração {i}")
		nome_tabela = os.path.splitext(arquivo)[0]

		if not inspect(engine).has_table(nome_tabela):
			df = pd.read_csv(os.path.join(folder_path, arquivo), encoding='latin1', sep=';')

		if dataset == 'escola':
			_padronizar_cols_escolas(df, arquivo)
			_converter_data(date_columns1, df)
			tipos_de_dados = _detect_column_types(df)

			tabela = Table(nome_tabela, 
						metadata, 
						*[Column(coluna, tipo_dado) for coluna, tipo_dado in tipos_de_dados.items()]
						)							
			tabela.create(bind=engine)
			df.to_sql(nome_tabela, engine, if_exists='replace', index=False)
				
			i+=1
			metadata.create_all(engine)

if __name__ == '__main__':
	carregar_dados_banco(arquivos_escolas_csv, folder_escolas, date_columns1)
#	carregar_dados_banco(arquivos_estudantes_csv, folder_estudantes, date_columns2)
