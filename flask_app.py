#-----------------------
# 匯入模組
#-----------------------
from flask import Flask, render_template, session 

#-----------------------
# 匯入各個服務藍圖
#-----------------------
from services.product.app import product_bp
from services.order.app import order_bp
from services.installment.app import installment_bp
from services.user.app import user_bp
from services.user.app import user_bp, login_manager

#-------------------------
# 產生主程式, 加入主畫面
#-------------------------
app = Flask(__name__)

# #加密(登入/登出)
app.config['SECRET_KEY'] = 'mykey'

#主畫面
@app.route('/')
def index():
    try:
        if session['username']:
            return render_template('index.html', name=session['username']) 
        else:
            return render_template('index.html', name='尚未登入')
    except:
        return render_template('index.html', name='尚未登入')
        

#-------------------------
# 在主程式註冊各個服務
# #-------------------------
app.register_blueprint(product_bp, url_prefix='/product')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(order_bp, url_prefix='/order')
app.register_blueprint(installment_bp, url_prefix='/installment')

login_manager.init_app(app) 
#-------------------------
# 啟動主程式
#-------------------------
if __name__ == '__main__':
    app.run(debug=True)