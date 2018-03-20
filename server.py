from flask import Flask, render_template, request, redirect, url_for
import csv, os
from data_manager import *

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def list_questions():
    return render_template('questions.html')


@app.route('/question/<id>')
def display_question():
    pass


@app.route('/form')
def form():
    return render_template('form.html', h1='Create answer')

@app.route('/form/<id>')
def form():
    return render_template('form.html', h1='Create answer')


if __name__ == '__main__':
    app.secret_key = "topsecret"
    answers = read_answers()
    app.run(debug=True, host='0.0.0.0', port=5000)
