from flask import Flask, render_template, request, redirect, url_for, abort
import csv, os, time
from data_manager import *
from werkzeug.utils import secure_filename
import sql_data_manager

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

column = "submisson_time"
desc = False


@app.route('/')
@app.route('/list')
@app.route('/search', methods=['GET'])
def list_questions():
    global column
    global desc
    order = request.args.get('order')
    column = order
    search_term = request.args.get('search_term')
    if column == order:
        if search_term:
            questions = sql_data_manager.search_questions(search_term, request.args.get('order'), desc)
        else:
            questions = sql_data_manager.read_questions(request.args.get('order'), desc)
        desc = not desc
    else:
        if search_term:
            questions = sql_data_manager.search_questions(search_term, order)
        else:
            questions = sql_data_manager.read_questions(order)
    
    return render_template('questions.html', questions=questions)


@app.route('/question/<int:id>')
def display_question(id):
    answer = sql_data_manager.read_answers_by_question_id(id)
    question = sql_data_manager.read_question_by_id(id)[0]
    question_comments = sql_data_manager.question_comments(id)
    
    if not question:
        abort(404)
    
    return render_template("answers.html", answer=answer, question=question, question_comments = question_comments)


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
            if file and allowed_file(file.filename):
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


if __name__ == '__main__':
    app.secret_key = "topsecret"
    app.run(debug=True, host='0.0.0.0', port=5000)
