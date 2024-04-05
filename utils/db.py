# 匯入連結資料庫模組
import psycopg2

# PostgreSQL連線資訊
DB_HOST = "tiny.db.elephantsql.com"
DB_NAME = "bmpeldyj"
DB_USER = "bmpeldyj"
DB_PASSWORD = "Sftrf0MFMmjxUjCZn0d1kDeIN1s471do"

# 建立資料庫連線
def get_connection():
    connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return connection