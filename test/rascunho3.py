import sqlite3
import pandas as pd

database_name ="../test_analytics.db"


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

df_escolas
df_estudantes

