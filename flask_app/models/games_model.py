from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model

class Game:
    db = "gamingwebsite_schema"
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price= data['price']
        self.productkey= data['productkey']
        self.image= data['image']

        

    @classmethod
    def newgame(cls,data):
        query="INSERT INTO games (title,description,price,productkey,image) VALUES ( %(title)s,%(description)s,%(price)s,%(productkey)s,%(image)s);"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results
    @classmethod 
    def getallgames(cls):
        query="SELECT * FROM games"
        results = connectToMySQL(cls.db).query_db(query)

        return  results
    

    @classmethod
    def deleteone(cls,data):
            query="DELETE FROM cart Where game_id=%(id)s"
            return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod 
    def getonegame(cls,data):
        query="SELECT * FROM games WHERE id=%(id)s"
        results = connectToMySQL(cls.db).query_db(query,data)

        return  cls(results[0])
    
    @classmethod 
    def getallcategories(cls):
        query="SELECT * FROM catergories"
        results = connectToMySQL(cls.db).query_db(query)
        print (results)

        return  results
    
    @classmethod
    def search(cls,data):
        query="SELECT * FROM games WHERE title LIKE %(title)s "
        results = connectToMySQL(cls.db).query_db(query,data)
        print (results)
        return results

        