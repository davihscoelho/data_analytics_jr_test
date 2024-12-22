import pandas as pd
import zipfile, os
import sqlite3
from sqlalchemy import create_engine, inspect, MetaData, Table, Column, String, Integer, Float, Date, text
import re

engine = create_engine("sqlite:///../test_analytics.db", echo=True)
metadata = MetaData()
metadata.reflect(bind=engine)

zip_file_path = "../Data/Data.zip"

with zipfile.ZipFile(zip_file_path, 'r') as zip:
  zip.extractall("../Data")

# Constants
folder_escolas  = "../Data/Data/Escolas"
folder_estudantes = "../Data/Data/Perfil dos educandos"
arquivos_escolas_csv = [arquivo for arquivo in os.listdir(folder_escolas) if arquivo.endswith('.csv')]
arquivos_estudantes_csv = [arquivo for arquivo in os.listdir(folder_estudantes) if arquivo.endswith(".csv")]
date_columns1 = ['dt_criacao', 'doc_criacao', 'dom_criacao', 'dt_ini_conv', 'dt_ini_func', 'dt_autoriza', 'dt_extincaoo', 'database']
date_columns2 = ['database']

def _padronizar_cols(df):
    cleaned_columns = []
    for col in df.columns:
        # Convert to lowercase
        col = col.lower()
        # # Replace spaces and special characters with underscores
        # col = re.sub(r'[^\w]+', '_', col)
        # # Ensure no leading/trailing underscores
        # col = col.strip('_')
        # # Add to cleaned list
        # cleaned_columns.append(col)
    
    # Rename DataFrame columns
    df.columns = cleaned_columns
    return df


def _converter_data(cols, df):
	for coluna in df.columns:
		if coluna in cols:
			df[coluna] = pd.to_datetime(df[coluna], format="%d/%m/%Y", errors='coerce')
		return df

def carregar_dados_banco(arquivos_csv, folder_path, date_columns):
	i = 0
	for arquivo in arquivos_csv:
		print(arquivo)
		print(f"Iteração {i}")
		nome_tabela = os.path.splitext(arquivo)[0]

		if not inspect(engine).has_table(nome_tabela):
			df = pd.read_csv(os.path.join(folder_path, arquivo), encoding='latin1', sep=';')
			df = _padronizar_cols(df)
			df = _converter_data(date_columns, df)

			tipos_de_dados =  {coluna: Date if pd.api.types.is_datetime64_any_dtype(df[coluna]) else
											Integer if pd.api.types.is_integer_dtype(df[coluna]) else
											Float if pd.api.types.is_float_dtype(df[coluna]) else
											String for coluna in df.columns}
			
			tabela = Table(nome_tabela, 
							metadata, 
							*[Column(coluna, tipo_dado) for coluna, tipo_dado in tipos_de_dados.items()]
							)							
			tabela.create(bind=engine)
			df.to_sql(nome_tabela, engine, if_exists='replace', index=False)
			
			i+=1
	metadata.create_all(engine)
	print(f"Dados da pasta {folder_path} carregados com sucesso")

if __name__ == '__main__':
	carregar_dados_banco(arquivos_escolas_csv, folder_escolas, date_columns1)
	carregar_dados_banco(arquivos_estudantes_csv, folder_estudantes, date_columns2)
		

#conn.close()



