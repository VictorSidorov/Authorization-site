from flask import Flask, render_template, request, json, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config["SECRET_KEY"] = "abc"
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:   
            user = Users.query.filter_by(email = request.form['email']).first()
            if user.password == request.form['password']:
                login_user(user)
                return redirect('/')
        except:
            return "Error"
    else:
        return render_template("login.html")


@app.route("/register", methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        _name = request.form['name']
        _email = request.form['email']
        _password = request.form['password']

        user = Users(name = _name, email = _email, password = _password)

        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/login') 
        except:
            return "Error"
 
    else:
        return render_template("register.html")


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)