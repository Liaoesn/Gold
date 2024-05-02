# 匯入Blueprint模組
from flask import request, render_template
from flask import Blueprint
import os
import uuid
import psycopg2

from utils import db, common
# from flask_login import login_required

# 產生產品服務藍圖
order_bp = Blueprint('order_bp', __name__)

#--------------------------
# 在產品服務藍圖加入路由
#--------------------------
#產品清單
@order_bp.route('/list')
# @login_required
def order_list(): 
    page = request.args.get('page', 1, type=int)
    per_page = 8

    # 計算偏移量
    offset = (page - 1) * per_page

     #取得資料庫連線 
    connection = db.get_connection() 
    cursor = connection.cursor()  
    
    cursor.execute('SELECT sales.*, product.proname FROM sales INNER JOIN product ON sales.prono = product.prono ORDER BY sales.soldno')
    
    total_data_count = cursor.fetchone()[0]

    total_pages = (total_data_count + per_page - 1) // per_page

    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    cursor.execute('''
        SELECT sales.*, product.proname 
        FROM sales 
        INNER JOIN product ON sales.prono = product.prono 
        ORDER BY sales.soldno 
        LIMIT %s OFFSET %s
    ''', (per_page, offset))
    
    #取出資料
    data = cursor.fetchall()    
    print(data)
    #關閉資料庫連線    
    connection.close() 
    
    #渲染網頁  
    return render_template('order/list.html', data=data, page=page, per_page=per_page, total_data_count=total_data_count,total_pages=total_pages)

