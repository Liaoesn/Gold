# 匯入模組
from flask import Blueprint, render_template, request, session
from flask_login import LoginManager, UserMixin, login_user, logout_user 
from flask import Blueprint

from utils import db

# 產生使用者服務藍圖
user_bp = Blueprint('user_bp', __name__)

#---------------------------
# (登入管理)使用者的類別
#---------------------------
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        
#---------------------------
# (登入管理)產生一個管理者
#---------------------------
login_manager = LoginManager()

#------------------------------
# (登入管理)取出登入者物件
#------------------------------
@login_manager.user_loader  
def user_loader(id): 
    return User(id) 
    
#---------------------------
# (登入管理)未授權頁面
#---------------------------
@login_manager.unauthorized_handler
def unauthorized():
    return render_template('unauthorized.html')

#---------------------------
# 使用者登入表單
#---------------------------
@user_bp.route('/login_form')
def login_form():
    return render_template('user/login_form.html')

#--------------------------
# 使用者登入
#--------------------------
@user_bp.route('/login', methods=['POST'])
def user_login():
    # 取出帳號/密碼
    account = request.form.get('account')
    passWord = request.form.get('passWord')
    
    # 建立資料庫連線
    conn = db.get_connection()
    
    # 查詢使用者
    cursor = conn.cursor()    
    cursor.execute("SELECT userName, userPW, isadmin FROM users WHERE userName = %s AND userPW = %s", (account, passWord))
    user = cursor.fetchone()
    
    # 判斷使用者是否存在
    if user:
        userName = user
        user = User(userName)   #(登入管理)產生一個user物件  
        login_user(user)     #(登入管理)在session中保存此user物件 
        session['account'] = userName #將使用者姓名放入對話中 
        return render_template('/index.html', username=userName)
    else:
        return render_template('/login_confirm.html', username=userName)
    
#---------------------------
# 登出
#---------------------------
@user_bp.route('/logout', methods=['GET'])
def logout():        
    logout_user()   #(登入管理)從session清除user物件
    session['account'] = None  #將使用者姓名從對話清除

    return render_template('/index.html')

#---------------------------
# 註冊畫面
# ---------------------------
@user_bp.route('/create')
def create():
    return render_template('user/create.html')

# @user_bp.route('/create/signin', methods=['POST'])
# def create_user():
#     try:
#         #取得其他參數
#         account = request.form.get('account')
#         passWord = request.form.get('passWord')
#         print(account)
#         print(passWord)

#         #取得資料庫連線
#         conn = db.get_connection()

#         #將資料加入user表
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO users (username,  userpw, isadmin) VALUES ( %s, %s, %s)",(account, passWord, 'a'))
#         conn.commit()
#         conn.close()

#         # 渲染成功畫面
#         return render_template('user/login.html')
#     except Exception as e:
#         #印出錯誤原因
#         print('-'*30)
#         print(e)
#         print('-'*30)
        
#         # 渲染失敗畫面
#         return render_template('create_fail.html')


#---------------------------
# 使用者表單
# ---------------------------
@user_bp.route('/list')
def list():
    page = request.args.get('page', 1, type=int)
    per_page = 8 

    # 計算偏移量
    offset = (page - 1) * per_page

    #取得資料庫連線 
    connection = db.get_connection() 
    cursor = connection.cursor() 
    
    cursor.execute('SELECT COUNT(*) FROM users')
    total_data_count = cursor.fetchone()[0] 

    #產生執行sql命令的物件, 再執行sql     
    cursor.execute('SELECT * FROM users ORDER BY userno LIMIT %s OFFSET %s', (per_page, offset))
    
    #取出資料
    data = cursor.fetchall()    
    print(data)
    #關閉資料庫連線    
    connection.close() 
    
    #渲染網頁  
    return render_template('user/list.html', data=data, page=page, per_page=per_page, total_data_count=total_data_count)

