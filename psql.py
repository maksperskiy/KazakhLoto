import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

connection = psycopg2.connect(user="postgres", password="password", port=15432)
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cursor = connection.cursor()

cursor.execute('create database kazakhloto')

cursor.close()
connection.close()
