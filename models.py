from extension import db
from sqlalchemy import and_, Enum
from datetime import datetime, timedelta, date

class User(db.Model):
    __tablename__ = 'user'
    # primary_key：主键    autoincrement：自增长
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 登录名  unique：唯一
    username = db.Column(db.String(32), unique=True)
    # 邮箱
    email = db.Column(db.String(32), unique=True)
    # 密码
    password = db.Column(db.String(32))
    # 角色   default：attendee
    role = db.Column(db.String(32), default="attendee")
    tickets = db.relationship("Ticket")
    def __repr__(self):
        return '<User %r %r %r>' % (self.username, self.password, self.role)

# 初始化数据库
    @staticmethod
    def init_db():
        users= [
                (1,"admin", "123@163.com", "123456", "organiser"),
                (2,"costom", "678@163.com", "123456", "attendee")
            ]
        for u in users:
            user = User()
            user.id = u[0]
            user.username = u[1]
            user.email = u[2]
            user.password = u[3]
            user.role = u[4]
            db.session.add(user)
        db.session.commit()    

    def insert_User(name, pwd, role, mail):
        newU = User()
        newU.username = name
        newU.email = mail
        newU.password = pwd
        newU.role = role
        db.session.add(newU)
        db.session.commit()

    def getUsersByName(name, pwd):
        user = User.query.filter(and_(User.username==name, User.password==pwd)).first()
        return user

    def getUserByEmail(email):
        user = User.query.filter_by(email=email).first()
        return user


class Activity(db.Model):
    __tablename__ = 'activity'
    # primary_key：主键    autoincrement：自增长
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 活动标题 
    title = db.Column(db.String(32))
    # 活动时间
    bgtime = db.Column(db.DateTime, default=datetime.now())
    endtime = db.Column(db.DateTime, default=datetime.now())
    # 活动状态
    status = db.Column(db.Enum('Canceled', 'Normal'),default='Normal')
    create_at = db.Column(db.DateTime, default=datetime.now())
    organiser = db.Column(db.String(100))
    # 活动描述
    description = db.Column(db.String(100), default="")
    number = db.Column(db.INTEGER, default=10)
    tickets = db.relationship("Ticket")
    def __repr__(self):
        return '<Activity %r %r %r %r %r %r>' % (self.id,self.title, self.bgtime, self.endtime, self.status, self.number)
    
    def insert_Activity(title, bgtime, endtime, status,description, organiser, number):
        newA = Activity()
        newA.title = title
        newA.bgtime = bgtime
        newA.endtime = endtime
        newA.status = status
        newA.description = description
        # 发起人名字
        newA.organiser = organiser
        newA.create_at = datetime.now()
        newA.number = number
        db.session.add(newA)
        db.session.commit()
        return newA.id

    # 初始化数据库
    @staticmethod
    def init_db():
        activities= [
                (1,"painting", datetime.now(), datetime.now()+timedelta(days=3),"Normal","desdes","admin", 2),
                (2,"hiking", datetime.now(), datetime.now()+timedelta(days=3),"Normal","desdes","admin", 5)
            ]
        for a in activities:
            activity = Activity()
            activity.id = a[0]
            activity.title = a[1]
            activity.bgtime = a[2]
            activity.endtime = a[3]
            activity.status = a[4]
            activity.description = a[5]
            activity.organiser = a[6]
            activity.numbe = a[7]
            db.session.add(activity)
        db.session.commit()  


# 活动和用户对应表
class Ticket(db.Model):
    __tablename__ = 'actiuser'
    # primary_key：主键    autoincrement：自增长
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 用户参与活动，得到的票据号
    ticketCode = db.Column(db.String(16), unique=True) 
    userId = db.Column(db.INTEGER,db.ForeignKey('user.id'))
    activityId = db.Column(db.INTEGER,db.ForeignKey('activity.id'))

    def __repr__(self):
        return '<Ticket %r %r %r>' % (self.ticketCode, self.userId, self.activityId)

    def insert_Ticket(userId, activityId, ticketNo):
        ticket = Ticket()
        ticket.userId = userId
        ticket.activityId = activityId
        ticket.ticketCode = ticketNo
        db.session.add(ticket)
        db.session.commit()
        return ticket.id   
    @staticmethod
    def init_db():
        tickets= [
                (1,1,"123434323423424356"),
                (1,2,"112114323423424356")
            ]
        for a in tickets:
            ticket = Ticket()
            ticket.userId = a[0]
            ticket.activityId = a[1]
            ticket.ticketCode = a[2]
            db.session.add(ticket)
            db.session.commit()  