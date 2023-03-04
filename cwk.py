from flask import Flask, render_template, request, redirect, url_for, flash, session, json
import sqlite3
from extension import db
from models import User, Activity, Ticket
from datetime import timedelta, datetime
from activity import ticketNumber
from sqlalchemy import and_

app = Flask(__name__)
app.secret_key = 'bjhenf#$%^kjn'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///activity.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2) 
app.config['SECRET_KEY'] ='cd5r456814r65ghtr223'
db.init_app(app)


# $env:FLASK_APP="cwk.py"
# 自定义指令
@app.cli.command()
def create():
   db.drop_all() #删除所有的数据表
   db.create_all()  #创建新数据表
   User.init_db()  #初始化User数据表
   Activity.init_db()
   Ticket.init_db()

#route to the index
@app.route('/index')
def index():
    with open('README.md') as readme:
      with open('requirements.txt') as req:
        username = session.get('username')
        userId = session.get('userId')
        if not username:
            return render_template('index.html', README=readme.read(), requirements=req.read(), name="Visiter")
        else:
             # 找到所有组织的活动
            username = session.get('username')
            activites = Activity.query.filter(Activity.organiser.contains(username)).all()
            # 计算已报名人数
            message = ''
            for act in activites:
                actId = act.id
                max = act.number
                number = Ticket.query.filter_by(activityId=actId).count()
                # 已经超过80%,添加到信息
                if number/max >= 0.8:
                    message = message + act.title + "has " + str(number) + " people, max is " + str(max) + ".   "
            #筛选所有已买的票
            joinAct = Ticket.query.filter_by(userId=userId).all()
            # 找对应活动，如果状态是cancel则显示信息
            for tick in joinAct:
                ticActi = Activity.query.filter_by(id=tick.activityId).all()
                for a in ticActi:
                    if a.status == "Canceled":
                        message = message + a.title + " had been Canceled!" + "   "
            if message:
                flash(str(message))
            return render_template('index.html', README=readme.read(), requirements=req.read(), name=username)

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        username = request.form.get('pesudo')
        pwd = request.form.get('pwd')
        user = User.getUsersByName(username,pwd)
        if not user:
            message = 'user or password incorrect'
            flash(message)
         # 登陆成功
        if user:
            session['username'] = username
            session['role'] = user.role
            session['userId'] = user.id
            return redirect(url_for('index'))
        else:
            return  redirect(url_for('login'))
          

# from models import User
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('register.html') 
    else:
        role = "attendee"
        if request.form.get('token') == 'Dc5_G1gz':
            role = 'organiser'
        pesudo = request.form.get('pesudo')
        email = request.form.get('email')
        pwd = request.form.get('pwd')
        if pesudo:
            if User.getUserByEmail(email):
                info = "User already exist!" 
                return render_template('register.html', error=info)
            else:
                info = ""
                User.insert_User(pesudo,pwd,role,email)
                return redirect(url_for('login'))
        else:
            redirect(url_for('register'))

@app.route("/activity", methods=['GET', 'POST'])
def activity():
    role = session.get('role')
    if request.method == "GET" :
        name = session.get('username')
        if not name:
            name = "Visiter"
        return render_template('activity.html', content = Activity.query.all(), name=name, role=role)
    else:
        # 从表单中获取数据，创建新活动，插入数据表
        data = json.loads(request.form.get('data'))
        title= data['title']
        number = data['number']
        status= data['status']
        des= data['des']
        endtime= data['endtime']
        endtime = endtime.replace('T',' ')
        endtime = endtime + ":00"
        end_time = datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S')
        bgtime= data['bgtime']
        bgtime = bgtime.replace('T',' ')
        bgtime = bgtime + ":00"
        begin_time = datetime.strptime(bgtime, '%Y-%m-%d %H:%M:%S')
        organiser = session.get('username')
        code = ticketNumber.getNumber()
        activityId = Activity.insert_Activity(title, begin_time, end_time, status,des,organiser,number)
        content=Activity.query.all()
        # 把新活动和活动组织者加入ticket表
        userid = session.get('userId')
        Ticket.insert_Ticket(userid, activityId,code)
        return render_template('activity.html', content=content)
    
@app.route('/details?<int:id>')
def details(id):
    session['activityId'] = id
    name = session.get('username')
    if not name:
        name = "Visiter"
    content=Activity.query.filter_by(id=id).first()
    number = Ticket.query.filter_by(activityId=id).count()
    return render_template('details.html', content=content, name=name, number=number)


# @app.route('/getSession',methods=['GET','POST'])
# def getSession():
#     name = session.get('username')
#     role = session.get('role')
#     id = session.get('userId')
#     user = {'username':name, 'role':role, 'id':id }
#     return user

@app.route('/buyTicket',methods=['GET','POST'])
def buyTicket():
    userid = session.get('userId')
    actId = session.get('activityId')
    code = ticketNumber.getNumber()
    Ticket.insert_Ticket(userid, actId,code)
    ticketInfo = {'username':userid, 'activityId':actId, 'code':code }
    return ticketInfo

@app.route("/myActivity", methods=['GET', 'POST'])
def myActivity():
    name = session['username']
    userid = session.get('userId')
    content = []
    # 找到用户组织的所有活动
    activites = Activity.query.filter(Activity.organiser.contains(name)).all()
    content=db.session.query(Ticket.ticketCode,Activity.title, Activity.id,Activity.organiser, Activity.bgtime, Activity.endtime, Activity.status).join(Activity, Ticket.activityId==Activity.id).filter(Ticket.userId==userid).all()
    return render_template('myActivity.html', orgcontent=activites, content=content,name=name)

@app.route('/participants?<int:id>',methods=['GET','POST'])
def participants(id):
    print(session)
    print(id)
    if request.method == "GET":
        session['activityId'] = id 
        # id = session['activityId']
        # 找到用户组织的所有活动的参与者信息
        name = session.get('username')
        content=db.session.query(Ticket.ticketCode, User.username, User.role, User.email, User.id).join(User, Ticket.userId==User.id).filter(Ticket.activityId==id).all()
        return render_template('participants.html', content=content,name=name)
    # else:
    #     # 用于修改参与者角色
    #     print("22222222222222")
    #     data = json.loads(request.form.get('data'))
    #     id= data['id']
    #     activityId = session['activityId']
    #     act =Activity.query.filter_by(id=activityId).first()
    #     user =User.query.filter_by(id=id).first()
    #     user.role="organiser"
    #     if not act.organiser.contains(user.username):
    #         act.organiser = act.organiser + "," +user.username
    #     db.session.commit()
    #     name = session.get('username')
    #     content=db.session.query(Ticket.ticketCode, User.username, User.role, User.email, User.id).join(User, Ticket.userId==User.id).filter(Ticket.activityId==id).all()
    #     return render_template('participants.html', content=content,name=name)
    
@app.route('/setRole?<int:id>')
def setRole(id):
    # 用于修改参与者角色
    activityId = session['activityId']
    act =Activity.query.filter_by(id=activityId).first()
    user =User.query.filter_by(id=id).first()
    user.role="organiser"
    act.organiser = act.organiser + "," +user.username
    db.session.commit()
    name = session.get('username')
    content=db.session.query(Ticket.ticketCode, User.username, User.role, User.email, User.id).join(User, Ticket.userId==User.id).filter(Ticket.activityId==id).all()
    return render_template('participants.html', content=content,name=name)

@app.route('/calcel',methods=['GET','POST'])
def calcel():
    data = json.loads(request.form.get('data'))
    id= int(data['activityId']) 
    act = Activity.query.filter_by(id=id).first()
    act.status = 'Canceled'
    db.session.commit()
    message = act.title + " has been canceled"
    flash(message)

@app.route('/refund',methods=['GET','POST'])
def refund():
    data = json.loads(request.form.get('data'))
    code= int(data['code']) 
    ticket = Ticket.query.filter_by(ticketCode=code).first()
    print(ticket)
    db.session.delete(ticket)
    db.session.commit()

if __name__ == "__main__":
    app.run()
    