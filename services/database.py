import pyodbc

server = 'DESKTOP-A3IBJIT'
database = 'ProjetoSISE'
username = 'sa'
password = 'ProjetoSISE'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
cursor = cnxn.cursor()