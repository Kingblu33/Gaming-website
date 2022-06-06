from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import games_model
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 



class User: 
    db = "gamingwebsite_schema"

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.gameinfo=[]


    @staticmethod
    def validate_info(form_data):
        is_valid=True
        if len(form_data["first_name"]) < 3 :
            flash("First Name needs to be more than three(3) characters")
            is_valid=False

        if len(form_data["last_name"]) < 3 :
            flash("last Name needs to be more than three(3) characters")
            is_valid=False
        if len(form_data["password"]) < 3 :
            flash("Password needs to be more than three(3) characters")
            is_valid=False
        if not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(form_data["password"]) < 5:
            flash("password needs to be longer than 5 characters")
            is_valid=False

        if form_data["password"] != form_data["confirm_password"]:
            flash("passwords dont match")
            is_valid=False

        return is_valid
    @classmethod
    def save_new_user(cls,data):
        query="INSERT INTO users (first_name,last_name,email,password) VALUES ( %(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results
    
    @classmethod
    def login(cls,data):
        query="SELECT * FROM users WHERE email=%(email)s;"
        results=connectToMySQL(cls.db).query_db(query,data)

        if len(results) < 1:
            return False

        return cls(results[0])
    @classmethod 
    def getoneusert(cls,data):
        query="SELECT * FROM users WHERE id=%(id)s"
        results = connectToMySQL(cls.db).query_db(query,data)

        return  cls(results[0])

    @classmethod
    def itemsincart(cls, data):
        query = "SELECT * FROM users LEFT JOIN cart ON cart.user_id = users.id LEFT JOIN games ON cart.game_id=games.id Where users.id= %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        print("results",results)
        games = cls( results[0] )
        for row_from_db in results:
            game_data = {
                "id" : row_from_db["games.id"],
                "title" : row_from_db["title"],
                "description" : row_from_db["description"],
                "price" : row_from_db["price"],
                "productkey" : row_from_db["productkey"],
                "image" : row_from_db["image"],

            }
            games.gameinfo.append( games_model.Game(game_data) )
        return games

    @classmethod
    def addtocart(cls,data):
        query="INSERT INTO cart (user_id,game_id) VALUES (%(users_id)s ,%(game_id)s);"

        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def sumofgames(cls,data):
        query="SELECT Count(*) as count, SUM(price) AS sum FROM games LEFT JOIN cart ON cart.game_id=games.id LEFT JOIN users ON cart.user_id = users.id Where users.id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        return results
    