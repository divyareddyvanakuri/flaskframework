from app import app
from flask_mysqldb import MySQL,MySQLdb
from MySQLdb.connections import OperationalError

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_PORT"]=3306
app.config["MYSQL_USER"]="Divya"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"]="flask"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql = MySQL(app)

def usernameauthentication(username):
    cur = mysql.connection.cursor()
    cur.execute( "SELECT * FROM auths WHERE username LIKE %s", (username,) )
    user = cur.fetchone()
    cur.close()
    return user
def emailauthentication(email):
    cur = mysql.connection.cursor()
    cur.execute( "SELECT * FROM auths WHERE email LIKE %s", (email,) )
    user = cur.fetchone()
    cur.close()
    return user

def createuser(username,email,hash_password):
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO  auths (username,email,password,is_active) VALUES(%s,%s,%s,false)",(username,email,hash_password,))
        mysql.connection.commit()     
        cur.close()
    except OperationalError as err:
        return "somthing went wrong"

def userauthentication(username):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM auths WHERE username LIKE %s", (username,) )
        user = cur.fetchone()
        print(user)
        cur.close()
        return user
    except OperationalError as err:
        return "somthing went wrong"
    
def activateaccount(email):
    cur = mysql.connection.cursor()
    cur.execute( "UPDATE auths SET is_active=true WHERE email LIKE %s",[email])
    mysql.connection.commit()
    cur.close()
    return "your account is activated"

def passwordupdation(hash_password,email):
    cur = mysql.connection.cursor()
    cur.execute( "UPDATE auths SET password=%s WHERE email LIKE %s", [hash_password,email,] )
    mysql.connection.commit()
    cur.close()