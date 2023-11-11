from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Tree: # MODEL AFTER TREES TABLE
    DB = "syvees_black_belt"
    def __init__(self, data):
        self.id = data["id"]
        self.species = data["species"]
        self.location = data["location"]
        self.reason = data["reason"]
        self.planted_date = data["planted_date"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.planter = None
        self.visitors = []
        self.number_of_visits = data["number_of_visits"]

    @classmethod # INSERT A TREE
    def save_tree(cls, data):
        query = """INSERT INTO trees (species, location, reason, planted_date, user_id) 
        VALUES (%(species)s, %(location)s, %(reason)s, %(planted_date)s, %(user_id)s )"""
        results = connectToMySQL(cls.DB).query_db(query, data)

    @classmethod # GET ALL TREES (ADVANCED) - DASHBOARD
    def get_all_trees_with_users(cls):
        query = """SELECT *, (SELECT COUNT(user_id) FROM visits WHERE visits.tree_id = trees.id) AS number_of_visits 
                FROM trees LEFT JOIN users ON users.id = trees.user_id"""
        results = connectToMySQL(cls.DB).query_db(query)
        trees = []
        for row in results:
            this_tree = cls(row)
            user_data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]
            }
            this_tree.planter = user.User(user_data)
            trees.append(this_tree)
        return trees
    
    @classmethod # UPDATE TREE
    def update_tree (cls,data):
        query = """UPDATE trees
                SET species=%(species)s, location=%(location)s, reason=%(reason)s, planted_date=%(planted_date)s
                WHERE trees.id = %(id)s"""
        result = connectToMySQL(cls.DB).query_db(query, data) 
        return result
    
    @classmethod # GET ONE TREE (ADVANCED) - DASHBOARD
    def get_one_tree_with_user(cls,data):
        query = """SELECT *, (SELECT COUNT(user_id) FROM visits WHERE visits.tree_id = trees.id) AS number_of_visits 
                FROM trees LEFT JOIN users ON users.id = trees.user_id WHERE trees.id = %(id)s"""
        results = connectToMySQL(cls.DB).query_db(query,data)
        for row in results:
            this_tree = cls(row)
            user_data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]
            }
            this_tree.planter = user.User(user_data)
        return this_tree
    
    @classmethod # GET ONE TREE WITH VISITS (ADVANCED) MANY TO MANY -- SHOW PAGE
    def get_trees_with_visitors (cls,data):
        query = """SELECT *, (SELECT COUNT(user_id) FROM visits WHERE visits.tree_id = trees.id) AS number_of_visits 
                FROM trees LEFT JOIN visits ON visits.tree_id = trees.id
                LEFT JOIN users ON users.id = visits.user_id  WHERE trees.id = %(id)s"""
        results = connectToMySQL(cls.DB).query_db(query,data)
        one_tree = cls(results[0]) # SINCE IT WILL ALWAYS HAVE AT LEAST ONE RESULT
        for row in results:
            if row["visits.user_id"] == None:
                return one_tree
            user_data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]
            }
            one_tree.visitors.append(user.User(user_data))
        return one_tree
    
    @classmethod # INSERT VISITED TREE
    def save_visit_tree(cls,data):
        query = "INSERT INTO visits (user_id, tree_id) VALUES (%(user_id)s, %(tree_id)s)"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod # DELETE A TREE
    def delete_tree (cls,data):
        query = "DELETE FROM trees WHERE id = %(id)s"
        result = connectToMySQL(cls.DB).query_db(query, data) 
        return result
    
    @staticmethod # NEW TREE VALIDATIONS
    def validate_add_tree(data): 
        is_valid = True
        if len(data["species"]) < 5:
            flash("Species should be at least 5 characters.", "add_tree")
            is_valid = False
        if len(data["location"]) < 2:
            flash("Location should be at least 2 characters.", "add_tree")
            is_valid = False
        if len(data["reason"]) < 1:
            flash("Please fill out the reason", "add_tree")
            is_valid = False
        if len(data["reason"]) > 50:
            flash("Reason should be maximum of characters.", "add_tree")
            is_valid = False
        if data["planted_date"] == "":
            flash("Please select a date.", "add_tree")
            is_valid = False
        return is_valid

