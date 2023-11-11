from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.tree import Tree
from flask_app.models.user import User
from flask_bcrypt import Bcrypt 
from flask import flash

@app.route("/dashboard") # GO TO DASHBOARD
def display_dashboard():
    if "logged_in_id" not in session: # CHECK IF IN SESSION
        return redirect ("/")
    all_trees = Tree.get_all_trees_with_users()
    data = {
        "id" : session["logged_in_id"]
    }
    one_user = User.get_one_by_id(data)
    return render_template("dashboard.html", all_trees=all_trees, one_user=one_user)

@app.route("/show/<int:tree_id>") # SHOW EACH TREE
def display_tree(tree_id):
    if "logged_in_id" not in session: # CHECK IF IN SESSION
        return redirect ("/")
    data = {
        "id" : tree_id  
    }
    show_tree = Tree.get_one_tree_with_user(data)
    tree_visitors = Tree.get_trees_with_visitors(data)
    return render_template("show.html", one_tree=show_tree, tree_visitors=tree_visitors)

@app.route("/new/tree") # RENDER BLANK TREE FORM
def display_tree_form():
    if "logged_in_id" not in session: # CHECK IF IN SESSION
        return redirect ("/")
    return render_template("new.html")

@app.route("/add/tree", methods=["POST"]) # ADD TREE AND POST
def add_tree():
    if "logged_in_id" not in session: # CHECK IF IN SESSION
        return redirect ("/")
    if not Tree.validate_add_tree(request.form): # VALIDATION AND RETURN TO ADD TREE FORM
        return redirect("/new/tree")
    data = {
            "species" : request.form["species"],
            "location" : request.form["location"],
            "reason" : request.form["reason"],
            "planted_date" : request.form["planted_date"],
            "user_id" : session["logged_in_id"]
        }
    Tree.save_tree(data)
    return redirect("/dashboard")

@app.route("/edit/<int:tree_id>") # RENDER EDIT TREE PRE-POPULATED
def edit_tree(tree_id):
    if "logged_in_id" not in session: # CHECK IF IN SESSION
        return redirect ("/")
    data = {
        "id":tree_id  
    }
    one_tree = Tree.get_one_tree_with_user(data)
    return render_template("edit.html", one_tree=one_tree)

@app.route("/update/<int:tree_id>", methods=["POST"]) # UPDATE THE TREE AND POST
def update_tree(tree_id):
    if "logged_in_id" not in session: # CHECK IF IN SESSION
        return redirect ("/")
    id = tree_id
    if not Tree.validate_add_tree(request.form): # VALIDATION AND RETURN TO INDEX
        return redirect(f"/edit/{id}")
    data = {
            "species" : request.form["species"],
            "location" : request.form["location"],
            "reason" : request.form["reason"],
            "planted_date" : request.form["planted_date"],
            "id" : id
        }
    Tree.update_tree(data)
    return redirect("/user/account")

@app.route("/delete/<int:tree_id>") # DELETE A TREE
def delete_tree(tree_id):
    if "logged_in_id" not in session: # CHECK IF IN SESSION
        return redirect ("/")
    data = {
        "id":tree_id  
    }
    Tree.delete_tree(data)
    return redirect("/user/account")

@app.route("/add/visit/<int:tree_id>") # ADD TREE VISIT
def save_visit_tree (tree_id):
    id = tree_id
    data = {
        "user_id" : session["logged_in_id"],
        "tree_id" : id
    }
    tree_id=id
    Tree.save_visit_tree(data)
    return redirect(f"/show/{tree_id}")