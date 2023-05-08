from flask import Flask
from flask import render_template, redirect, flash, request, session

import bcrypt
import sqlite3
import os

app = Flask(__name__)

db = sqlite3.connect('database.db', check_same_thread=False)

initCursor = db.cursor()
initCursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='users';")

if len(initCursor.fetchall()) != 1:
    # The database has not been intialized
    initCursor.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL, balance INTEGER);")
    initCursor.execute(
        "CREATE TABLE items (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, price INTEGER NOT NULL, location INTEGER NOT NULL, qty_remain INTEGER NOT NULL, calories INTEGER NOT NULL, last_sale DATETIME);")

    db.commit()

initCursor.close()

app.secret_key = os.environ["FLASK_KEY"] if "FLASK_KEY" in os.environ != "" else "n0t_s3cure_k3y"


@app.route("/")
def index():
    if "id" in session:
        return redirect("/home")
    return render_template("index.html")


@app.route("/login")
def login():
    if "id" in session:
        return redirect("/home")
    else:
        return render_template("login.html")


@app.route("/register")
def register():
    if "id" in session:
        return redirect("/home")
    else:
        return render_template("register.html")


@app.route("/login", methods=['POST'])
def do_login():
    if len(request.form['password']) == 0 or len(request.form['username']) == 0:
        flash("You must enter both a username and a password.", "warning")
        return login()
    else:
        c = db.cursor()
        c.execute("SELECT id, password FROM users WHERE username = ?", [
            request.form['username']])
        row = c.fetchone()
        c.close()
        if (row == None):
            flash("Invalid login", "warning")
            return login()
        elif (bcrypt.checkpw(str.encode(request.form['password']), row[1])):
            session['id'] = row[0]
            return redirect("/home")
        else:
            flash("Invalid login", "warning")
            return login()


@app.route('/register', methods=['POST'])
def do_register():
    if len(request.form['password']) == 0 or len(request.form['username']) == 0:
        flash("You must enter a username and password.", "danger")
    else:
        username = request.form['username']
        password = request.form['password']
        c = db.cursor()
        c.execute("SELECT id FROM users WHERE username = ?", [username])
        if len(c.fetchall()) != 0:
            flash("That username has already been used.", "danger")
        else:
            hashedPassword = bcrypt.hashpw(
                str.encode(password), bcrypt.gensalt())
            c.execute("INSERT INTO USERS (username, password, balance) VALUES (?, ?, 0);",
                      [username, hashedPassword])
            db.commit()
            c.close()
            flash("You've signed up, now log in.", "success")
            return redirect("/login")
        c.close()
    return register()


@app.route("/home")
def home():
    if not "id" in session:
        flash("You must login to access that page", "warning")
        return login()
    else:
        return render_template("home.html")


@app.route("/logout", methods=['POST'])
def do_logout():
    del session["id"]
    flash("You have been logged out.", "info")
    return redirect("/")


@app.route("/items")
def items():
    if not "id" in session:
        flash("You must login to access that page", "warning")
        return login()
    else:
        c = db.cursor()
        c.execute("SELECT * FROM items ORDER BY location DESC")
        data = [{"id": item[0], "name": item[1], "price": int(item[2])/100, "location": item[3],
                 "qty_remain": item[4], "calories": item[5], "last_purchase": item[6]} for item in c.fetchall()]
        c.close()
        print(data)
        return render_template("items.html", items=data)


@app.route("/newItem", methods=["POST"])
def new_item():
    if not "id" in session:
        flash("You must login to access that page", "warning")
        return login()
    elif (not "name" in request.form or
          not "price" in request.form or
          not "location" in request.form or
          not "qty_remain" in request.form or
          not "calories" in request.form):
        flash("All fields are required", "warning")
        return items()
    else:
        c = db.cursor()
        c.execute("INSERT INTO items (name, price, location, qty_remain, calories) VALUES (?, ?, ?, ?, ?)",
                  [request.form["name"], int(request.form["price"])*100, request.form["location"], request.form["qty_remain"], request.form["calories"]])
        c.close()
        db.commit()
        flash("Item added!", "success")
        return items()


@app.route("/updateItem", methods=["POST"])
def update_item():
    if not "id" in session:
        flash("You must login to access that page", "warning")
        return login()
    elif (
            not "id" in request.form or
            not "name" in request.form or
            not "price" in request.form or
            not "location" in request.form or
            not "qty_remain" in request.form or
            not "calories" in request.form):
        flash("All fields are required", "warning")
        return items()
    else:
        c = db.cursor()
        c.execute("UPDATE items SET name = ?, price = ?, location = ?, qty_remain = ?, calories = ? WHERE id = ?",
                  [request.form["name"], float(request.form["price"])*100, request.form["location"], request.form["qty_remain"], request.form["calories"], request.form["id"]])
        c.close()
        db.commit()
        flash("Item updated", "success")
        return items()
