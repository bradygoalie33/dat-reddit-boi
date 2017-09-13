import pyodbc

#uncertain how python works with params and if concat is needed
def execute_query(driver, server, db, query)
	connection = pyodbc.connect("Driver={driver};"
								"Server=server;"
								"Database=db;"
								"Trusted_Connection=yes")

	cursor = connection.cursor()
	cursor.execute('query')
#return something? do something?