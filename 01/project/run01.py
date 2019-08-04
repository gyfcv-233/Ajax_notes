from flask import Flask, make_response, request,render_template,session,redirect
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@localhost:3306/flask'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] =True
app.config['SECRET_KEY'] = 'INPUT A STRING'
db = SQLAlchemy(app)


@app.route('/create_xhr')
def create_xhr():
    return render_template('xhr.html')
if __name__ == '__main__':
    app.run(debug=True)