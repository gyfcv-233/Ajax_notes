from flask import Flask, render_template,request
import json
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost:3306/flask"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] =True
db = SQLAlchemy(app)


class Province(db.Model):
    __tablename__="province"
    id = db.Column(db.Integer,primary_key=True)
    proname = db.Column(db.String(30),nullable=False)
    cities = db.relationship("City",backref="province",lazy ="dynamic")

    def to_dict(self):
        dic = {
            "id":self.id,
            "proname":self.proname
        }
        return dic

    def __init__(self,proname):
        self.proname = proname

    def __repr__(self):
        return "<Province %r>" % self.proname

class City(db.Model):
    __tablename__ = "city"
    id = db.Column(db.Integer,primary_key=True)
    cityname = db.Column(db.String(30),nullable=False)
    pro_id = db.Column(db.Integer,db.ForeignKey("province.id"))

    def to_dict(self):
        dic = {
            'id':self.id,
            'cityname':self.cityname,
            'pro_id':self.pro_id
        }
        return dic
    def __init__(self,cityname,pro_id):
        self.cityname = cityname
        self.pro_id = pro_id

    def __repr__(self):
        return "<City %r>" % self.cityname
db.create_all()


@app.route('/01-province')
def province_views():
    return render_template('01-province.html')

@app.route('/01-loadPro')
def loadPro01_views():
    provinces = db.session.query(Province).all()
    list =[]
    for pro in provinces:
        list.append(pro.to_dict())
    return json.dumps(list)

@app.route('/02-loadCity')
def loadCity_views():
    #接收前端传递过来的数据,pid为前端传递过来的参数名
    pid = request.args.get('pid')
    cities = db.session.query(City).filter_by(pro_id=pid).all()
    list = []
    for city in cities:
        list.append(city.to_dict())
    return json.dumps(list)

@app.route('/03-load')
def load_views():
    return render_template('03-load.html')
@app.route('/03-server',methods=["POST"])
def server_03():
    #// var params = "name=sf.zhang&age=85";  //get 方式
    # name = request.args["name"]
    # age = request.args["age"]
    name = request.form["name"]
    age = request.form["age"]
    return "姓名：%s,年龄：%s" %(name,age)

@app.route('/04-get')
def get_views():
    return render_template("04-get.html")
@app.route('/04-server')
def server_04():
    cities = City.query.all()
    list = []
    for city in cities:
        list.append(city.to_dict())
    return json.dumps(list)


################分隔区#################3
@app.route('/05-server')
def server_05():
    cityname = request.args.get('cityname')
    cities = db.session.query(City).filter_by(cityname=cityname).first()
    if cities:
        return json.dumps(cities.to_dict())
    else:
        dic ={
            'status':"0",
            "msg":"查找的用户不存在"
        }
        return json.dumps(dic)


# 非同源请求
@app.route('/06-server')
def server_06():
    # 接收前端传递过来的callback即前端处理响应数据的函数名
    cb = request.args.get('callback')
    # 响应数据，被前端页面当成js脚本被执行
    return cb+"('这是server_06响应回来的数据')"

@app.route('/07-server')
def sever_07():
    cb = request.args.get('callback')
    dic = {
        'filghtNO':'MU763',
        'from':'bejing',
        'to':'Saipan',
        'time':'16:55'
    }
    # flight('{ 'filghtNO':'MU763','from':'bejing'.....}')
    return cb +"(" + json.dumps(dic) + ")"


if __name__ == "__main__":
    app.run(debug=True)