from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] 

# 访问网站的地址
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

if __name__ == "__main__":
    app.run()