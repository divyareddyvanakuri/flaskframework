from flask import Flask,render_template,request,session
from flask_mysqldb import MySQL,MySQLdb
from MySQLdb.connections import OperationalError
import bcrypt

app = Flask(__name__)

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
      password = request.form["password"]
      cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cur.execute("SELECT * FROM users WHRERE username=%s",(username,))
      user = cur.fetchone()
      print(user)
      cur.close()
      if len(user)>0:
         if (password,user["password"]) == user["password"]:
            session["username"] = user["username"]
            session["email"] = user["email"]
      else:
         return "Error password and user not match"
   return render_template("login.html")

@app.route('/register',methods=["GET","POST"])
def register():
   if request.method == "POST":
      username=request.form["username"]
      email=request.form["email"]
      password=request.form["password"]
      confirmpassword=request.form["confirmpassword"]
      cur = mysql.connection.cursor()
      #cur.execute('''CREATE TABLE users (username VARCHAR(30),email VARCHAR(50),password VARCHAR(100))''')
      cur.execute("INSERT INTO  users (username,email,password) VALUES(%s,%s,%s)",(username,email,password))
      mysql.connection.commit()
      session["username"] = username      
      cur.close()
      return "successfully registered"
   return render_template("register.html")

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
   app.secret_key="exobts2020@#$$^&(@!#^("
   app.run(debug=True)
