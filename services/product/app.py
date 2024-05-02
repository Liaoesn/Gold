# 匯入Blueprint模組
from flask import request, render_template
from flask import Blueprint
import os
import uuid
import psycopg2

from utils import db, common
# from flask_login import login_required

# 產生產品服務藍圖
product_bp = Blueprint('product_bp', __name__)

#--------------------------
# 在產品服務藍圖加入路由
#--------------------------
#產品清單
@product_bp.route('/list')
# @login_required
def product_list(): 
    page = request.args.get('page', 1, type=int)
    per_page = 8

    # 計算偏移量
    offset = (page - 1) * per_page

     #取得資料庫連線 
    connection = db.get_connection() 
    cursor = connection.cursor()  
    
    cursor.execute('SELECT * FROM product order by prono')
    
    total_data_count = cursor.fetchone()[0]

    total_pages = (total_data_count + per_page - 1) // per_page

    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    cursor.execute('SELECT * FROM product ORDER BY prono LIMIT %s OFFSET %s', (per_page, offset))

    #取出資料
    data = cursor.fetchall()    
    print(data)
    #關閉資料庫連線    
    connection.close() 
    
    #渲染網頁  
    return render_template('product/list.html', data=data, page=page, per_page=per_page, total_data_count=total_data_count,total_pages=total_pages)


#產品查詢表單
@product_bp.route('/read/form')
# @login_required
def product_read_form():
    return render_template('product_read_form.html') 


#產品查詢
@product_bp.route('/read', methods=['GET'])
# @login_required
def product_read():    
    #取得資料庫連線    
    connection = db.get_connection()  
    
    #取得執行sql命令的cursor
    cursor = connection.cursor()   
    
    #取得傳入參數, 執行sql命令並取回資料  
    prono = request.values.get('prono').strip()
      
    cursor.execute('SELECT * FROM product WHERE prono=%s', (prono,))
    data = cursor.fetchone()

    #關閉連線   
    connection.close()  
        
    #渲染網頁
    if data:
        return render_template('product_read.html', data=data) 
    else:
        return render_template('not_found.html')
    
    
#產品新增表單
@product_bp.route('/add')
# @login_required
def product_create_form():
    return render_template('product/add.html') 


#產品新增
@product_bp.route('/create', methods=['POST'])
# @login_required
def product_create():
    try:
        #取得上傳圖檔
        photo = request.files['photo']
        filename = None
        
        #檢查是否有選擇圖片, 並且檔案類型允可
        if photo and common.allowed_file(photo.filename):
            #產生一個唯一的檔名並儲存它
            filename = str(uuid.uuid4()) + '.' + photo.filename.rsplit('.', 1)[1].lower()
            photo.save(os.path.join('static/photos', filename))        
        
        #取得其他參數
        proname = request.form.get('proname')
        goldprice = request.form.get('goldprice')
        sugprice = request.form.get('sugprice')
        manual = request.form.get('manual')
        state = request.form.get('state')


        #取得資料庫連線
        conn = db.get_connection()

        #將資料加入product表
        cursor = conn.cursor()
        cursor.execute("INSERT INTO product (proname,  goldprice, sugprice, manual, state, photo) VALUES ( %s, %s, %s, %s, %s, %s)",
                        (proname,  goldprice, sugprice, manual, state,  psycopg2.Binary(filename)))
        conn.commit()
        conn.close()

        # 渲染成功畫面
        return render_template('create_success.html')
    except Exception as e:
        #印出錯誤原因
        print('-'*30)
        print(e)
        print('-'*30)
        
        # 渲染失敗畫面
        return render_template('create_fail.html')

    
#產品刪除表單
@product_bp.route('/delete/form')
# @login_required
def product_delete_form():
    return render_template('product_delete_form.html') 


#產品刪除確認
@product_bp.route('/delete/confirm', methods=['GET'])
# @login_required
def product_delete_confirm():
    #取得資料庫連線    
    connection = db.get_connection()  
    
    #取得執行sql命令的cursor
    cursor = connection.cursor()   
    
    #取得傳入參數, 執行sql命令並取回資料  
    prono = request.values.get('prono').strip()
      
    cursor.execute('SELECT * FROM product WHERE prono=%s', (prono,))
    data = cursor.fetchone()

    #關閉連線   
    connection.close()  
        
    #渲染網頁
    if data:
        return render_template('product_delete_confirm.html', data=data) 
    else:
        return render_template('not_found.html')
    
    
#產品刪除
@product_bp.route('/delete', methods=['POST'])
# @login_required
def product_delete():
    try:
        #取得參數
        prono = request.form.get('prono').strip().upper()

        #取得資料庫連線
        conn = db.get_connection()

        #將資料從product表刪除
        cursor = conn.cursor()
        cursor.execute("DELETE FROM product WHERE prono = %s", (prono,))
        
        conn.commit()
        conn.close()

        # 渲染成功畫面
        return render_template('delete_success.html')
    except Exception as e:
        #印出錯誤原因
        print('-'*30)
        print(e)
        print('-'*30)
        
        # 渲染失敗畫面
        return render_template('delete_fail.html')    

    
#產品更改表單
@product_bp.route('/update/form')
# @login_required
def product_update_form():
    return render_template('product_update_form.html') 


#產品更改確認
@product_bp.route('/update/confirm', methods=['GET'])
# @login_required
def product_update_confirm():
    #取得資料庫連線    
    connection = db.get_connection()  
    
    #取得執行sql命令的cursor
    cursor = connection.cursor()   
    
    #取得傳入參數, 執行sql命令並取回資料  
    prono = request.values.get('prono').strip().upper()
      
    cursor.execute('SELECT * FROM product WHERE prono=%s', (prono,))
    data = cursor.fetchone()

    #關閉連線   
    connection.close()  
        
    #渲染網頁
    if data:
        return render_template('product_update_confirm.html', data=data) 
    else:
        return render_template('not_found.html')
    
    
#產品更改
@product_bp.route('/update', methods=['POST'])
# @login_required
def product_update():
    try:
        #取得參數
        prono = request.form.get('prono')
        proname = request.form.get('proname')
        goldprice = request.form.get('goldprice')
        sugprice = request.form.get('sugprice')
        manual = request.form.get('manual')
        state = request.form.get('state')

        #取得資料庫連線
        conn = db.get_connection()

        #將資料從product表刪除
        cursor = conn.cursor()
        cursor.execute("UPDATE product SET proname=%s, goldprice=%s, sugprice=%s, manual=%s, state=%s WHERE prono = %s", (proname, goldprice, sugprice, manual, state, prono))
        
        conn.commit()
        conn.close()

        # 渲染成功畫面
        return render_template('update_success.html')
    except Exception as e:
        #印出錯誤原因
        print('-'*30)
        print(e)
        print('-'*30)
        
        # 渲染失敗畫面
        return render_template('update_fail.html')      