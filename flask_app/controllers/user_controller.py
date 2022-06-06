from flask_app import app
from flask import render_template, session, redirect, request
from flask_app.models.user_model import User
from flask_app.models.games_model import Game
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def defaultroute():
    if 'userid' not in session:
        flash("please login")
        return(redirect('/login'))
    query_data = {
        "id": session['userid']
    }
    user = User.getoneusert(query_data)
    games = Game.getallgames()
    category = Game.getallcategories()
    return render_template('dashboard.html', user=user, games=games, category=category)


@app.route('/cart')
def cart():
    if 'userid' not in session:
        flash("please login")
        return(redirect('/login'))

    query_data = {
        "id": session['userid']
    }
    cart = User.itemsincart(query_data)
    sum_results = User.sumofgames(query_data)
    sum = sum_results[0]['sum']
    count = sum_results[0]['count']
    print(cart)
    return render_template('cart.html', cart=cart, sum=sum, count=count)


@app.route('/addtocart/<int:id>')
def addtocart(id):
    query_data = {
        "users_id": session['userid'],
        "game_id": id
    }
    User.addtocart(query_data)
    return redirect('/')


@app.route('/register')
def register():

    return render_template('register.html')
# ===============================================================
# register route
# ===============================================================


@app.route('/registration', methods=["POST"])
def regis():

    if not User.validate_info(request.form):
        return redirect('/register')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print("pw_hash")
    query_data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash,
    }

    userid = User.save_new_user(query_data)
    session['userid'] = userid
    return redirect('/')


@app.route('/login')
def logging():
    return render_template('login.html')
# ===============================================================
# login route
# ===============================================================


@app.route('/loginin', methods=['POST'])
def login():

    data = {"email": request.form["email"]}
    user_in_db = User.login(data)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):

        flash("Invalid Email/Password")
        return redirect('/')
    print(data)

    session['userid'] = user_in_db.id

    return redirect("/")


@app.route('/logout')
def logout():

    session.clear()

    return render_template('/login.html')
