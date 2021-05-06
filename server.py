from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlite3 import Connection as SQLite3Connection
from sqlalchemy import event
from sqlalchemy.engine import Engine
from datetime import datetime
import linked_list
import hash_table
import binary_search_tree
import custom_queue
import stack
import random

app = Flask(__name__) # Middleware that sits between the python aplication and the server
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0

# Configure slite3 to enforce foreign key constrains
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_key=ON;")
        cursor.close()

db = SQLAlchemy(app)
now = datetime.now()

# Models
class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    post = db.relationship("BlogPost", cascade="all, delete")

class BlogPost(db.Model):
    __tablename__ = "BlogPost"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(250))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)

# Routes
@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(name=data["name"], email=data["email"], address=data["address"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message" : "User Created"}), 200

@app.route("/user/descending_id", methods=["GET"])
def get_all_users_descending():
    users = User.query.all()
    all_users = linked_list.LinkedList()

    for user in users:
        all_users.insert_beginning({
            "id" : user.id,
            "name" : user.name,
            "email" : user.email,
            "address" : user.address,
        })
    return jsonify(all_users.to_list()), 200

@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_ascending():
    users = User.query.all()
    all_users = linked_list.LinkedList()

    for user in users:
        all_users.insert_end({
            "id" : user.id,
            "name" : user.name,
            "email" : user.email,
            "address" : user.address,
        })
    return jsonify(all_users.to_list()), 200

@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id):
    users = User.query.all()
    all_users = linked_list.LinkedList()

    for user in users:
        all_users.insert_beginning({
            "id" : user.id,
            "name" : user.name,
            "email" : user.email,
            "address" : user.address,
        })
    user = all_users.get_user_by_id(user_id)
    return jsonify(user), 200

@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"message" : "User does not exist, or already been deleted"}), 400
    db.session.delete(user)
    db.session.commit()
    return jsonify({}), 200

@app.route("/blog_post/<user_id>", methods=["POST"])
def create_blog_post(user_id):
    data = request.get_json()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "User does not exist!"}), 400
    
    ht = hash_table.HashTable(10)
    ht.add_key_value("title", data["title"])
    ht.add_key_value("body", data["body"])
    ht.add_key_value("date", now)
    ht.add_key_value("user_id", user_id)

    new_blog_post = BlogPost(title=ht.get_value("title"), body=ht.get_value("body"), date=ht.get_value("date"), user_id=ht.get_value("user_id"))
    db.session.add(new_blog_post)
    db.session.commit()
    return jsonify({"message" : "new blog post created"}), 200

@app.route("/blog_post/<blog_post_id>", methods=["GET"])
def get_one_blog_post(blog_post_id):
    blog_posts = BlogPost.query.all()
    random.shuffle(blog_posts)
    bts = binary_search_tree.BinarySearchTree()

    for post in blog_posts:
        bts.insert({
            "id" : post.id,
            "title" : post.title,
            "body" : post.body,
            "user_id" : post.user_id
        })
    
    post = bts.search(blog_post_id)
    if not post:
        return jsonify({"message" : "Post not found!"})
    
    return jsonify(post)

@app.route("/blog_post/numeric_body", methods=["GET"])
def get_numeric_post_bodies():
    blog_posts = BlogPost.query.all()
    q = custom_queue.Queue()

    for post in blog_posts:
        q.enqueue(post)
    return_list = []

    for _ in range(len(blog_posts)):
        post = q.dequeue()
        numeric_body = 0
        for char in str(post.data.body):
            numeric_body += ord(char)
        post.data.body = numeric_body

        return_list.append({
            "id" : post.data.id,
            "title" : post.data.title,
            "body" : post.data.body,
            "user_id" : post.data.user_id
        })
    return jsonify(return_list)

@app.route("/blog_post/delete_last_10", methods=["DELETE"])
def delete_last_10():
    blog_posts = BlogPost.query.all()
    s = stack.Stack()

    for post in blog_posts:
        s.push(post)
    
    for _ in range(10):
        post_to_delete = s.pop()
        db.session.delete(post_to_delete.data)
        db.session.commit()
    
    return jsonify({"message" : "success"})

if __name__ == "__main__":
    app.run(debug=True) # Start debug to True