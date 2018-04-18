from flask import Flask, render_template, request, redirect, url_for, abort, Blueprint, session, flash
import sql_data_manager

user_page = Blueprint('user_page', __name__, template_folder='templates')


@user_page.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        
        if sql_data_manager.check_if_user_exists(request.form["username"]):
            flash("User exists!", "error")
            return redirect(url_for("user_page.registration"))
        else:
            data = sql_data_manager.registration(request.form["username"], request.form["password"])
            
            if data:
                session["username"] = data["username"]
                flash("Successfull registration!", "success")
                return redirect(url_for("list_questions"))
    
    return render_template("registration.html")


@user_page.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if sql_data_manager.login(request.form["username"], request.form["password"]):
            session["username"] = request.form["username"]
            flash("Successfull login!", "success")
            return redirect(url_for("list_questions"))
        else:
            flash("No user found with :(", "error")
            return redirect(url_for("user_page.login"))
    
    return render_template("login.html")


@user_page.route("/logout", methods=["GET"])
def logout():
    if "username" in session:
        session.pop("username")
    
    return redirect(url_for("list_questions"))
