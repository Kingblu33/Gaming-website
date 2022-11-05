
from flask_app import app
from flask import render_template, session, redirect, request
from flask_app.models.games_model import Game
from flask_app.models.user_model import User
from werkzeug.utils import secure_filename


@app.route('/games')
def dash():
    if 'userid' not in session:
        flash("please login")
        return(redirect('/login'))
    return render_template('addgame.html')


@app.route('/addnewgame', methods=['post'])
def newgame():
    f = request.files['image']
    f.save(os.path.join('flask_app\static\image', secure_filename(f.filename)))
    query_data = {
        "title": request.form['title'],
        "description": request.form['description'],
        "price": int(request.form['price']),
        "productkey": request.form['productkey'],
        "image": f.filename,
    }
    Game.newgame(query_data)

    return redirect("/")


@app.route('/delete/<int:id>')
def delete(id):
    if 'userid' not in session:
        flash("please login")
        return(redirect('/login'))
    query_data = {
        "id": id
    }
    Game.deleteone(query_data)
    return redirect('/cart')


@app.route('/checkout')
def checkout():
    query_data = {
        "id": session['userid']
    }
    cart = User.itemsincart(query_data)
    return render_template('/checkout.html', cart=cart)


@app.route('/showone/<int:id>')
def showgame(id):
    query_data = {
        "id": id
    }
    game = Game.getonegame(query_data)
    return render_template('/showonegame.html', game=game)


@app.route('/search/game')
def search():
    return render_template('search.html')


@app.route('/search', methods=['post'])
def searchinput():
    query_data = {
        "title": request.form['search'] + "%%"
    }
    search = Game.search(query_data)

    return render_template('/search.html', search=search)
