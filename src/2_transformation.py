import pandas as pd
import duckdb 
import sqlite3
from datetime import datetime


database_name ="../test_analytics.db"
duckdb_database = "../my_database.duckdb"

def returning_df_from_all_tables(query):
	try:

		conn = sqlite3.connect(database_name)
		cursor = conn.cursor()

		cursor.execute (query)
		tables = [table[0] for table in cursor.fetchall()]

		if not tables:
			print ("Not is possible")

		union_all_query = " UNION ALL ".join(f"SELECT * FROM \"{table}\"" for table in tables)
		#cursor.execute(union_all_query)

		# rows = cursor.fetchall()
		df = pd.read_sql_query(union_all_query, conn)

		return df

	except sqlite3.Error as e:
		print(f"SQLITE error: {e}")

	finally:
		if conn:
			conn.close()


query =   """
  SELECT name FROM sqlite_master
  WHERE type = 'table' AND  (name LIKE 'escolas%' OR name LIKE '%escolas%');
  """

query2 = """
  SELECT name FROM sqlite_master
  WHERE type = 'table' AND  (name LIKE 'idadeserie%' OR name LIKE '%idadeserie%');
  """

df_escolas = returning_df_from_all_tables(query)
df_estudantes = returning_df_from_all_tables(query2)

conn = duckdb.connect(duckdb_database)
conn.execute("CREATE TABLE IF NOT EXISTS raw_escolas AS SELECT * FROM  df_escolas")
conn.execute("CREATE TABLE IF NOT EXISTS raw_estudantes AS SELECT * FROM df_estudantes")

escola = conn.sql(
  """
    SELECT DISTINCT
      re.dre,
      re.codesc,
      re.tipoesc,
      re.nomesc,
      re.diretoria,
      re.fx_etaria,
      re.situacao,
      re.database,
      re.dt_criacao ,
      re.dt_ini_conv ,
      re.cep
    FROM main.raw_escolas re
    WHERE re.fx_etaria IS NOT NULL
    ORDER BY re.codesc;
  """
  )

endereco = conn.sql(
  """
    SELECT DISTINCT
      re.endereco ,
      re.bairro ,
      re.distrito,
      re.coddist,
      re.cep,
      re.latitude ,
      re.longitude ,
      
    FROM main.raw_escolas re
    WHERE re.fx_etaria IS NOT NULL
    ORDER BY re.codesc;
  """
  )

estudantes = conn.sql(

  """
    SELECT * FROM main.raw_estudantes
  """
)

df_escola = escola.to_df()
df_endereco = endereco.to_df()
df_estudantes = estudantes.to_df()

def translate_brazilian_month(date_str):
    """Replace Brazilian month abbreviations with numeric equivalents."""
    if not isinstance(date_str, str):  # Check if the value is a string
        return date_str  # Return the original value (e.g., None)
    
    for pt_month, num_month in month_map.items():
        if pt_month in date_str:
            return date_str.replace(pt_month, num_month)
    return date_str

def parse_date(date_str):
      """Try to parse the date string into a standardized format."""
      date_str = date_str.strip().lower()
      formats = [
          "%d/%m/%Y",    # DD/MM/YYYY
          "%d/%m/%y",    # DD/MM/YY
          "%d/%b/%y",    # DD/Mon/YY (abbreviated month)
          "%d/%m/%Y %H:%M"  # DD/MM/YYYY HH:MM
      ]
      for fmt in formats:
          try:
              return datetime.strptime(date_str, fmt).date()
          except ValueError:
                continue
      return None  # Return None if parsing fails


def cleaning_df_escola(new_df):
	df = new_df.copy()
	month_map = {
		"jan": "01", "fev": "02", "mar": "03", "abr": "04",
		"mai": "05", "jun": "06", "jul": "07", "ago": "08",
		"set": "09", "out": "10", "nov": "11", "dez": "12"
		}
	categorical_columns = df.select_dtypes(include=['object', 'category']).columns
	date_columns = ["dt_criacao","dt_ini_func", "dt_ini_conv","dt_autoriza","database"]
	categorical_columns = categorical_columns.difference(date_columns)
	# Upper All columns
	df[categorical_columns] = df[categorical_columns].apply(lambda x: x.str.upper())

	# Change from ',' to '.' and strip for nomeesc
	df["nomesc"] = df["nomesc"].str.replace(",", "")
	df["nomesc"] = df["nomesc"].str.strip()

	df = df.dropna(subset=['database', "dt_criacao"])
	df["dt_ini_conv"] = df["dt_ini_conv"].fillna("01/01/2099")

	df['dt_criacao'] = (
		df['dt_criacao']
		.apply(translate_brazilian_month)  # Replace Brazilian months
		.apply(parse_date)  # Parse the dates
	)

	df['database'] = (
		df['database']
		.apply(translate_brazilian_month)  # Replace Brazilian months
		.apply(parse_date)  # Parse the dates
	)

	df['dt_ini_conv'] = (
		df['dt_ini_conv']
		.apply(translate_brazilian_month)  # Replace Brazilian months
		.apply(parse_date)  # Parse the dates
	)
  
	#data_cleaned["dt_criacao"] = pd.to_datetime(data_cleaned["dt_criacao"], format="%Y-%m")
	df['database'] = pd.to_datetime(df['database']).dt.to_period('M').astype(str)
	df['dt_criacao'] = pd.to_datetime(df['dt_criacao']).dt.to_period('M').astype(str)
	df['dt_ini_conv'] = pd.to_datetime(df['dt_ini_conv']).dt.to_period('M').astype(str)
	df = df.drop_duplicates(subset=['codesc','nomesc','dt_criacao'])

	return df

def cleaning_df_endereco(new_df):
	aux = new_df.copy()

	aux = df_endereco.drop_duplicates(subset=["cep","latitude","longitude"])
	aux['endereco'] = aux['endereco'].str.replace('Ã', 'Í').str.replace('ÃƒÂ', 'Í').str.replace('Ã', 'A').str.strip()
	aux['endereco'] = aux['endereco'].str.replace('Avenida', 'AVENIDA', case=False)
	aux['endereco'] = aux['endereco'].str.replace(r'\s+', ' ', regex=True).str.strip()
	aux = aux.drop_duplicates(subset=['endereco', 'cep', 'latitude', 'longitude'], keep='first')
	aux = aux.drop_duplicates(subset='endereco')
	aux = aux.drop_duplicates(subset='cep')
	
	return aux
