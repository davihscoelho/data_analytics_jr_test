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
file_path = "../Data/Data/Escolas/dicionarioescolas.xlsx"

df = pd.read_excel(file_path)
padrao_cols = df["CAMPO"].to_list()
padrao_cols = [x.lower() for x in padrao_cols]
set1 = set(padrao_cols)



dicionario = {}

for arquivo in arquivos_escolas_csv:
  #pd.read_csv(os.path.join(folder_path, arquivo), encoding='latin1', sep=';')
  df = pd.read_csv(os.path.join(folder_escolas, arquivo), encoding='latin1', sep=';')
  print(f"Arquivo: {arquivo}")
  cols_df = df.columns
  cols_df = [x.lower() for x in cols_df]
  set2 = set(cols_df)
  # Tem na lista original e não tem na tabela atual => Adicionar to NUll
  unique_values_1 = set1.difference(set2)
  # Tem na tabela atual, não tem na tabela original => Excluir ou Alterar
  unique_values_2 = set2.difference(set1)
  
  dicionario[arquivo] = (unique_values_1, unique_values_2)


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

dicionario2 = {}
for arquivo in arquivos_escolas_csv:
  new_df = pd.read_csv(os.path.join(folder_escolas, arquivo), encoding='latin1', sep=';')
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
  set2 = set(new_df.columns)
  # Tem na lista original e não tem na tabela atual => Adicionar to NUll
  unique_values_1 = set1.difference(set2)
  # Tem na tabela atual, não tem na tabela original => Excluir ou Alterar
  unique_values_2 = set2.difference(set1)
  
  dicionario2[arquivo] = (unique_values_1, unique_values_2)


dicionario.keys()
dicionario["escolas-dez-2010.csv"]
dicionario2["escolas-dez-2010.csv"]
dicionario["escolas-dez-2011.csv"]
dicionario2["escolas-dez-2011.csv"]
dicionario["escolas-dez-2012.csv"]
dicionario2["escolas-dez-2012.csv"]
dicionario["escolas-dez-2013.csv"]
dicionario2["escolas-dez-2013.csv"]
dicionario["escolas-dez-2014.csv"]
dicionario2["escolas-dez-2014.csv"]
dicionario["escolas-dez-2015.csv"]
dicionario2["escolas-dez-2015.csv"]


dicionario["escolas122018.csv"]
dicionario2["escolas122018.csv"]
dicionario["escolas122019.csv"]
dicionario2["escolas122019.csv"]
dicionario["escolas122020.csv"]
dicionario2["escolas122020.csv"]
dicionario["escolas122021.csv"]
dicionario2["escolas122021.csv"]
dicionario["escolas122022.csv"]
dicionario2["escolas122022.csv"]
dicionario["escolas122023.csv"]
dicionario2["escolas122023.csv"]


dicionario["escolasr34.csv"]
dicionario2["escolasr34.csv"]
dicionario["escolasr34dez2017.csv"]
dicionario2["escolasr34dez2017.csv"]