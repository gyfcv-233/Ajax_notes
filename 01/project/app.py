from flask import Flask, make_response, request,render_template,session,redirect
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@localhost:3306/flask'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] =True
app.config['SECRET_KEY'] = 'INPUT A STRING'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    uname = db.Column(db.String(50),nullable=False)
    upwd = db.Column(db.String(50), nullable=False)
    realname = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return "<User %r>" % self.uname
@app.route('/01-getxhr')
def get_xhr():
    return render_template("01-getxhr.html")

@app.route('/02-get')
def get_views():
    return render_template('02-get.html')
@app.route('/02-server')
def server02():
    return '这是AJAX的请求'

#练习
@app.route('/03-get')
def get03_views():
    return render_template('03-get.html')
@app.route('/03-server')
def server03_views():
    uname = request.args['uname']
    return "欢迎："+uname

#post
@app.route('/04-post')
def post_views():
    return render_template('04-post.html')
@app.route('/04-server',methods=['POST'])
def server04_views():
    uname = request.form['uname']
    age = request.form['age']
    return "姓名：%s，年龄：%s" %(uname,age)
@app.route('/05-post')
def post05_views():
    return render_template('05-post.html')


#post练习
@app.route('/06-post')
def post06_views():
    return  render_template('06-post.html')
@app.route('/06-server',methods=["POST"])
def server06_views():
    uname = request.form["uname"]
    user = db.session.query(User).filter_by(uname=uname).first()
    if user:
        return "用户名称已存在"
    else:
        return "通过"

@app.route('/array')
def array_views():
    return render_template('array.html')

if __name__ == "__main__":
    app.run(debug=True)