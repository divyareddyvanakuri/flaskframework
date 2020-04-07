from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_mysqldb import MySQL,MySQLdb
from MySQLdb.connections import OperationalError
from flask_mail import Mail,Message
from flask_shorturl import ShortUrl
from werkzeug.security import generate_password_hash,check_password_hash
import datetime
import jwt
import uuid



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
      token = str(uuid.uuid4())
      cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      result=cur.execute( "SELECT * FROM users WHERE email LIKE %s", (email,) )
      
      if result>0:
         user = cur.fetchone()
         msg = Message(subject="forgot password request",sender="divyavanakuri48@gmail.com",recipients=[email])
         msg.body = render_template("sent.html",token=token,data=user)
         mail.sent(msg)   
         cur = mysql.connection.cursor()
         cur.execute( "UPDATE users SET token=%s WHERE email LIKE %s", [token,email] )
         mysql.connection.commit()
         cur.close()
         flash("Email already sent to your email,successfully")
         return redirect('/forgotpassword')
      else:
         flash("Email do not match","danger")
   return render_template("forgotpassword.html")

@app.route('/reset/<token>',methods=["GET","POST"])
def reset(token):
   if request.method == "POST":
      password = request.form["password"]
      confirmpassword = request.form["confirmpassword"]
      token1 = str(uuid.uuid4())
      cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cur.execute( "SELECT * FROM users WHERE email LIKE %s", (token,) )
      user = cur.fetchone()
   return render_template("resetpassword.html")

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
