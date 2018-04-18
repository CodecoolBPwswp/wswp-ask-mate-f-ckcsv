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
