from flask import Flask,render_template,request,session,redirect,url_for
from flask_mysqldb import MySQL,MySQLdb
from MySQLdb.connections import OperationalError
from flask_mail import Mail
from flask_shorturl import ShortUrl
from werkzeug.security import generate_password_hash,check_password_hash
import datetime
import jwt



app = Flask(__name__)
mail = Mail(app)
app.config["SECRET_KEY"]="exobts2020@#$%^^&"
#mysql database connection 
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_PORT"]=3306
app.config["MYSQL_USER"]="Divya"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"]="flask"
app.config["MYSQL_CURSORCLASS"]="DictCursor"

mysql = MySQL(app)

@app.route('/')
def home():
   return render_template("home.html")

@app.route('/login',methods=["GET","POST"])
def login():
   if request.method == "POST":
      username = request.form["username"]
      print(username)
      password = request.form["password"]
      cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      # cur.execute("SELECT * FROM users WHRERE username=%s",[username])
      cur.execute( "SELECT * FROM users WHERE username LIKE %s", (username,) )
      user = cur.fetchone()
      print(user)
      cur.close()
      if check_password_hash(user["password"], password,method="sha256"):
         session["username"] = user["username"]
         session["email"] = user["email"]
         return render_template("home.html")
      else:
         return "Error password and user not match"
   return render_template("login.html")

@app.route("/logout")
def logout():
   session.clear()
   return render_template("home.html")

@app.route('/register',methods=["GET","POST"])
def register():
   if request.method == "POST":
      username=request.form["username"]
      email=request.form["email"]
      password=request.form["password"]
      confirmpassword=request.form["confirmpassword"]
      hash_password = generate_password_hash(password,method="sha256")
      print(hash_password)
      cur = mysql.connection.cursor()
      #cur.execute('''CREATE TABLE users (username VARCHAR(30),email VARCHAR(50),password VARCHAR(100))''')
      cur.execute("INSERT INTO  users (username,email,password) VALUES(%s,%s,%s)",(username,email,hash_password))
      mysql.connection.commit()
      # session["username"] = username      
      cur.close()
      return "Registeration done successfully"
   return render_template("register.html")

@app.route('/forgotpassword',methods=["GET","POST"])
def forgotpassword():
   if request.method == "POST":
      email = request.form["email"]
      cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      # cur.execute("SELECT * FROM users WHRERE username=%s",[username])
      cur.execute( "SELECT * FROM users WHERE email LIKE %s", (email,) )
      user = cur.fetchone()
      print(user)
      cur.close()
      token = tokenActivation(user["username"])
      surl = url_for(token,_external=True)
      print(surl)
      print(token)
      return "please check mail"
   return render_template("forgotpassword.html")

def tokenActivation(username):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': username
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e



@app.route('/database')
def database():
   try:
      cur = mysql.connection.cursor()
      # cur.execute('''CREATE TABLE example (id INTEGER ,name VARCHAR(20))''')
      cur.execute("INSERT INTO  example (id,name) VALUES(%s,%s)",("2","divyareddy"))
      mysql.connection.commit()
      cur.close()
      return "Table is created"
   except OperationalError:
      return "Table already existed"

if __name__ == '__main__':
   app.run(debug=True)
