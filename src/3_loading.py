import pandas  as pd
import duckdb 

duckdb_database = "../my_database.duckdb"
output_file = "../Data/output/dataset.csv"
conn = duckdb.connect(duckdb_database)

tab = conn.sql(
  """
    SELECT DISTINCT *  
    FROM main.escolas_alunos;
  """
  )

df = tab.fetchdf()

df.info()
columns_to_drop = ['database_1','rede_1',"codcie","codinep", "codesc_1", "subpref", "setor"]
df.drop(columns=columns_to_drop, inplace=True)
df.drop_duplicates().info()

df.to_csv(output_file, index=False)