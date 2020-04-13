from flask import Flask,render_template,request,session,redirect,url_for,flash
from app import app
from flask_mail import Mail,Message
from flask_shorturl import ShortUrl
from werkzeug.security import generate_password_hash,check_password_hash
import datetime
import jwt
import uuid
from flask_wtf.csrf import CSRFProtect,CSRFError
from .form import LogInForm,SignUpForm,ForgotPasswordForm,ResetPasswordForm
from .qurey import  userauthentication,usernameauthentication,emailauthentication,createuser,activateaccount,passwordupdation
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
import os


s = URLSafeTimedSerializer('Thisissecret!')
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

app.config.update(
	MAIL_DEBUG =True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
   MAIL_USE_TLS = False,
	MAIL_USERNAME = 'divyavanakuri48@gmail.com',
	MAIL_PASSWORD = os.environ['EMAIL_PASSWORD'],
   MAIL_DEFAULT_SENDER = 'divyavanakuri48@gmail.com'
	)
mail = Mail(app)
csrf = CSRFProtect(app)

@app.route('/')
def home():
   return render_template("home.html")

@app.route('/login',methods=["GET","POST"])
def login():
   form = LogInForm()
   if form.validate_on_submit():
      username = form.username.data
      password = form.password.data
      user = userauthentication(username)
   try:
      if check_password_hash(user["password"], password) and user['is_active']:
         session["username"] = user["username"]
         session["email"] = user["email"]
         return render_template("home.html")
      else:
         return "Error password and user not match or else user was not active"
   except UnicodeError as err:
      flash("somthing went wrong:",err)

   return render_template("login.html",form=form)

@app.route("/logout")
def logout():
   session.clear()
   return render_template("home.html")

@app.route('/register',methods=["GET","POST"])
@csrf.exempt
def register():
   form=SignUpForm()
   if form.validate_on_submit():
      username = form.username.data
      email = form.email.data
      password = form.password.data
      confirmpassword = form.confirmpassword.data
      if usernameauthentication(username):
         return "username should be unique"
      if emailauthentication(email):
         return "email id should be unique"
      if password == confirmpassword:
         hash_password = generate_password_hash(password,method="sha256")
         createuser(username,email,hash_password)
      token = s.dumps(email,salt='email-confirm')
      msg = Message('Activate',sender='divyavanakuri48@gmail.com',recipients=[email])
      link = url_for('activate',token=token,_external=True)
      msg.body = render_template("activate.html",link=link,email=email)
      print(msg)
      mail.send(msg)
      return "registeration done successfully,please activate account through mailed link"
   return render_template("register.html",form=form)

@app.route('/activate/<token>',methods=["GET","POST"])
def activate(token):
   try:
      email = s.loads(token,salt='email-confirm')
      print(email)
      user = emailauthentication(email)
      print(user)
      if user:
         activateaccount(email)
      else:
         return "invalide details"
      return "Your account activated successfully,please login"
   except SignatureExpired:
      return '<h1>the token is expired</h1>'
   

@app.route('/forgotpassword',methods=["GET","POST"])
def forgotpassword():
   if request.method == "POST":
      email = request.form["email"]
      token = s.dumps(email,salt='email-confirm')
      msg = Message('ResetPassword',sender='divyavanakuri48@gmail.com',recipients=[email])
      link = url_for('resetpassword',token=token,_external=True)
      msg.body = render_template("sent.html",link=link,email=email)
      print(msg)
      mail.send(msg)
      return "Email was sent successfully to your account"
   return render_template('forgotpassword.html')


@app.route('/resetpassword/<token>')
def resetpassword(token):
   if request.method == "POST":
      password = request.form["password"]
      confirmpassword = request.form["confirmpassword"]
      try:
         email = s.loads(token,salt='email-confirm')
         print(email)
         user = emailauthentication(email)
         print(user)
         if user: 
            hash_password = generate_password_hash(password,method="sha256")  
            passwordupdation(email,hash_passowrd)
         else:
            return redirect("/")
      except SignatureExpired:
         return '<h1>the token is expired</h1>'
      # flash("your password successfully updated","success")
      return redirect('/login')
   return render_template("resetpassword.html")


if __name__ == '__main__':
   app.run(debug=True)