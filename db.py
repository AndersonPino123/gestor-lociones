import psycopg2

def conectar():
    return psycopg2.connect(
        host="localhost",
        database="gestor_contactos",
        user="postgres",
        password="1030622188"
    )