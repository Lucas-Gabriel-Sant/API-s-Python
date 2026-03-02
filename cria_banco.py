import sqlite3

connection = sqlite3.connect('instance/banco.db')
cursor = connection.cursor()

cria_tabela = "CREATE TABLE IF NOT EXISTS hoteis (hotel_id text PRYMARY KEY,\
nome text, ranking real, diaria real, estado text)"

cria_hotel = "INSERT INTO hoteis VALUES ('lupus', 'Lupus Hotel', 4.7, 562, 'Rondonia')"

cursor.execute(cria_tabela)
cursor.execute(cria_hotel)

connection.commit()
connection.close()
