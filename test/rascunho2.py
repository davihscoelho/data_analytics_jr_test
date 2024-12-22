import pandas as pd
import zipfile
import os
import re

folder_escolas  = "../Data/Data/Escolas"
folder_estudantes = "../Data/Data/Perfil dos educandos"
arquivos_escolas_csv = [arquivo for arquivo in os.listdir(folder_escolas) if arquivo.endswith('.csv')]
arquivos_estudantes_csv = [arquivo for arquivo in os.listdir(folder_estudantes) if arquivo.endswith(".csv")]
date_columns1 = ['dt_criacao', 'doc_criacao', 'dom_criacao', 'dt_ini_conv', 'dt_ini_func', 'dt_autoriza', 'dt_extintao', 'database']
date_columns2 = ['database']
file_path = "../Data/Data/Perfil dos educandos/dicionariopefileducando.xlsx"

df = pd.read_excel(file_path)
padrao_cols = df["CAMPO "].to_list()
padrao_cols = [x.lower() for x in padrao_cols]
set1 = set(padrao_cols)
padrao_cols

rename_padrao = {
      "setedu":"setor",
      "codes": "codesc",
      "qtd": "qtde",
      "ï»¿dre": "dre"
      }

dicionario = {}

for arquivo in arquivos_estudantes_csv:
  #pd.read_csv(os.path.join(folder_path, arquivo), encoding='latin1', sep=';')
  df = pd.read_csv(os.path.join(folder_estudantes, arquivo), encoding='latin1', sep=';')
  print(f"Arquivo: {arquivo}")
  cols_df = df.columns
  cols_df = [x.lower() for x in cols_df]

  
  set2 = set(cols_df)
  # Tem na lista original e não tem na tabela atual => Adicionar to NUll
  unique_values_1 = set1.difference(set2)
  # Tem na tabela atual, não tem na tabela original => Excluir ou Alterar
  unique_values_2 = set2.difference(set1)
  
  dicionario[arquivo] = (unique_values_1, unique_values_2)

dicionario = {}
for arquivo in arquivos_estudantes_csv:
  #pd.read_csv(os.path.join(folder_path, arquivo), encoding='latin1', sep=';')
  new_df = pd.read_csv(os.path.join(folder_estudantes, arquivo), encoding='latin1', sep=';')
  cols_df = new_df.columns
  cols_df = [x.lower() for x in cols_df]
  new_df.columns = cols_df
  new_df = new_df.rename(columns = rename_padrao)
  
  if arquivo == "idadeserieneeracadez23.csv":
    new_df["raca"] = None
  cols_df = new_df.columns 
  
  set2 = set(cols_df)
  # Tem na lista original e não tem na tabela atual => Adicionar to NUll
  unique_values_1 = set1.difference(set2)
  # Tem na tabela atual, não tem na tabela original => Excluir ou Alterar
  unique_values_2 = set2.difference(set1)
  dicionario[arquivo] = (unique_values_1, unique_values_2)

dicionario.keys()
# df.head()
# pd.read_csv(os.path.join(folder_estudantes, arquivos_estudantes_csv[0]), encoding='latin1', sep=';').head()
dicionario["idadeserieneeraca-r33.csv"]
dicionario["idadeserieneeracadez17.csv"]
dicionario["idadeserieneeracadez18.csv"]
dicionario["idadeserieneeracadez19.csv"]
dicionario["idadeserieneeracadez20.csv"]
dicionario["idadeserieneeracadez21.csv"]
dicionario["idadeserieneeracadez22.csv"]
dicionario["idadeserieneeracadez23.csv"]


