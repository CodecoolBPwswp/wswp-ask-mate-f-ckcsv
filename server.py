from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)

@app.route('/')
@app.route('/list')
def list_questions():
    return render_template('questions.html')


@app.route('/question/<id>')
def display_question(id):
    answers = data_manager.read_answers()
    return render_template("answers.html", id=id, answers=answers[1])


if __name__ == '__main__':
    app.secret_key = "topsecret"
    app.run(debug=True, host='0.0.0.0', port=5000)
