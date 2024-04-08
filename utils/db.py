# 匯入連結資料庫模組
import psycopg2

# PostgreSQL連線資訊
DB_HOST = "rain.db.elephantsql.com"
DB_NAME = "ibznuobh"
DB_USER = "ibznuobh"
DB_PASSWORD = "oJk2pZcVs-QdYOSv_AniiToYi3ZArrhw"

# 建立資料庫連線
def get_connection():
    connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return connection
try:
    # 建立資料庫連線
    connection = get_connection()

    # 建立 cursor 物件
    cursor = connection.cursor()

    # 執行 SQL 查詢
    cursor.execute("SELECT username, userpw, isadmin FROM users LIMIT 1")

    # 檢索結果
    row = cursor.fetchone()
    
    # 輸出結果
    print("成功連接到資料庫，並且查詢結果為:", row)

    # 關閉 cursor 和連線
    cursor.close()
    connection.close()

except (Exception, psycopg2.Error) as error:
    print("連接失敗，錯誤訊息:", error)