from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
   return "Hello World"

@app.route('/login')
def login():
   return "Please login"

@app.route('/register')
def register():
   return "Please register"



if __name__ == '__main__':
   app.run(debug=True)
