import pyodbc

server = 'SE-CGS-520070'
database = 'ProjetoSISE'
username = 'sa'
password = 'ProjetoSISE'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
cursor = cnxn.cursor()