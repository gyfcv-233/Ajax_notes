from flask import Flask, render_template
import json
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost:3306/flask"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] =True
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ ="user"
    id = db.Column(db.Integer,primary_key=True)
    uname = db.Column(db.String(50))
    upwd = db.Column(db.String(50))
    realname = db.Column(db.String(30))

    #声明函数-将当前对象中的所有属性封装到一个字典中
    def to_dict(self):
        dic = {
            'id':self.id,
            'uname':self.uname,
            'upwd':self.upwd,
            'realname':self.realname
        }
        return dic

    def __repr__(self):
        return "<User %r>" % self.uname

db.create_all()



@app.route('/json')
def json_views():
    list = ["dasdh","dgbdsd", 'cat','ynasng']
    dic = {
        "name":"nanzi",
        'age':'20'
    }
    uList = [
        {
            "name": "nanzi",
            'age': '20'
        },
        {
            "name":"小新",
            'age':5
        }
    ]
    jsonStr = json.dumps(list)
    jsonuList = json.dumps(uList)
    return jsonuList


@app.route('/page')
def page_views():
    return  render_template('01-page.html')



@app.route('/json_user')
def json_user():
   # user = db.session.query(User).filter_by(id=1).first()  #可以
   # return json.dumps(user.to_dict())
   user = db.session.query(User).filter_by(id=1).all() #列表
   list = []
   for u in user:
       list.append(u.to_dict())
   return json.dumps(list)

#练习
@app.route('/02-index')
def index():
    return render_template('02-index.html')
@app.route('/01-server')
def user_all():
    user = db.session.query(User).all()
    list = []
    for u in user:
        list.append(u.to_dict())
    return json.dumps(list)


if __name__ == "__main__":
    app.run(debug=True)