from flask import Flask
from flask_mysqldb import MySQL


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
   return "Hello World"

@app.route('/login')
def login():
   return "Please login"

@app.route('/register')
def register():
   return "Please register"

@app.route('/database')
def database():
   cur = mysql.connection.cursor()
   cur.execute('''CREATE TABLE example (id INTEGER ,name VARCHAR(20))''')
   # mysql.connection.commit()
   cur.close()
   return "Done!"
if __name__ == '__main__':
   app.run(debug=True)
