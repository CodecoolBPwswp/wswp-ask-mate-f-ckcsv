from flask import Flask, render_template, request, redirect, url_for
import csv, os

app = Flask(__name__)

@app.route('/')
@app.route('/list')
def list_questions():
    return "YOLO"
    #questions = data_manager.

    #return render_template("questions.html", questions )



if __name__ == '__main__':
    app.secret_key = "topsecret"
    app.run(debug=True, host='0.0.0.0', port=5000)
