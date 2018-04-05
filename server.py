import os

from flask import Flask, render_template, request, redirect, url_for, abort
from werkzeug.utils import secure_filename

import sql_data_manager

UPLOAD_FOLDER = sql_data_manager.UPLOAD_FOLDER
app = Flask(__name__)

desc = False
order = "submisson_time"


@app.route('/')
@app.route('/list', methods=['GET'])
def list_questions():
    global desc
    global order
    
    if request.args.get('order') == order:
        desc = not desc
    else:
        order = request.args.get("order") if request.args.get("order") else "submisson_time"
    ascdesc = "DESC" if desc else "ASC"
    
    questions = sql_data_manager.read_questions(order, ascdesc)
    
    return render_template('questions.html', questions=questions)


@app.route('/question/<int:id>', methods=['GET', 'POST'])
def display_question(id):
    answer = sql_data_manager.read_answers_by_question_id(id)
    question = sql_data_manager.read_question_by_id(id)[0]
    answer_comments = sql_data_manager.answer_comments(id)
    
    if not question:
        abort(404)
    
    if request.method == "POST":
        sql_data_manager.add_comment(id, request.form["answer_id"], request.form["message"])
        return redirect(url_for("display_question", id=id) + "#" + request.form["answer_id"])


    return render_template("answers.html", answer=answer, question=question, answer_comments = answer_comments)


@app.route('/add-question')
@app.route('/add-question', methods=['POST'])
def question_form():
    if request.method == 'POST':
        sql_data_manager.write_question(request.form.get('title'), request.form.get('message'))
        return redirect(url_for('list_questions'))
    
    return render_template('add-question.html', h1='Create question')


@app.route('/question/<int:question_id>/new-answer')
@app.route('/question/<int:question_id>/new-answer', methods=['POST'])
def answer_form(question_id):
    if request.method == 'POST':
        filename = ''
        file = None
        if request.files:
            file = request.files['file']
            if file and sql_data_manager.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.getcwd() + os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        message = request.form.get('message')
        image = UPLOAD_FOLDER + filename if file else ''
        
        sql_data_manager.write_answer(question_id, message, image)
        return redirect('/question/{}'.format(question_id))
    
    return render_template('new-answer.html', h1='Create answer')


@app.route('/question/<question_id>/edit')
@app.route('/question/<question_id>/edit', methods=['POST'])
def edit_question(question_id):
    question = sql_data_manager.read_question_by_id(question_id)[0]
    
    if request.method == 'POST':
        try:
            question['title'] = request.form.get('title', '')
            question['message'] = request.form.get('message', '')
            
            sql_data_manager.update_question(question_id, question['title'], question['message'])
            
            return redirect('/question/{}'.format(question_id))
        except Exception as e:
            print(e)
    
    return render_template('add-question.html', edit_data={
        'title'  : question['title'],
        'message': question['message']
    })


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/question/<int:question_id>/<type>', methods=['POST'])
def vote(question_id, type):
    answer_id = request.form["answer_id"]
    sql_data_manager.update_vote(answer_id, type)
    return redirect(url_for("display_question", id=question_id))


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    sql_data_manager.delete_question(question_id)
    return redirect(url_for("list_questions"))


@app.route('/delete_answer/<answer_id>', methods=['POST'])
def delete_answer(answer_id):
    question_id = sql_data_manager.delete_answer(answer_id)
    return redirect(url_for("display_question", id=question_id))


def highlight(text: str, term: str):
    return text.replace(
            term.title(), "<mark>" + term.title() + "</mark>"
    ).replace(
            term.lower(), "<mark>" + term.title() + "</mark>"
    ).replace(
            term.upper(), "<mark>" + term.title() + "</mark>"
    )


@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('search_term', None)
    search_term = search_term.lower()
    
    if not search_term:
        return redirect(url_for('list_questions'))
        
    questions = sql_data_manager.search_questions(search_term)
    
    for question in questions:
        question['title'] = highlight(question['title'], search_term)
        question['message'] = highlight(question['message'], search_term)
    
    return render_template('search.html', questions=questions)


@app.route('/answer/<answer_id>/edit')
@app.route('/answer/<answer_id>/edit', methods=['POST'])
def edit_answer(answer_id):
    answer = sql_data_manager.read_answer_by_id(answer_id)[0]

    if request.method == 'POST':
        try:
            answer['message'] = request.form.get('message', '')

            sql_data_manager.update_answer(answer_id, answer['message'])

            question_id = sql_data_manager.read_question_id_by_answer_id(answer_id)[0]['question_id']

            return redirect('/question/{}'.format(question_id))
        except Exception as e:
            print(e)

    return render_template('new-answer.html', edit_data={
        'message': answer['message']
    })


if __name__ == '__main__':
    app.secret_key = "topsecret"
    app.run(debug=True, host='0.0.0.0', port=5000)
