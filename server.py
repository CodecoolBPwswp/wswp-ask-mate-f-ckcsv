from flask import Flask, render_template, request, redirect, url_for
import csv, os

app = Flask(__name__)

@app.route('/')
def list_questions():
    return render_template('questions.html')


@app.route('/question/<id>')
def display_question()
    pass


if __name__ == '__main__':
    app.secret_key = "topsecret"
    app.run(debug=True, host='0.0.0.0', port=5000)
