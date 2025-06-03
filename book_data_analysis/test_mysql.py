import mysql.connector

try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='booksDB',
        database='books_dataDB'
    )
    print("Conexão MySQL bem sucedida!")
    conn.close()
except mysql.connector.Error as err:
    print(f"Erro ao conectar ao MySQL: {err}")
except Exception as e:
    print(f"Erro inesperado: {e}")

input("Pressione ENTER para sair...")
