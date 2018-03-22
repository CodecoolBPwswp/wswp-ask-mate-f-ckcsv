from flask import Flask, render_template, request, redirect, url_for, abort
import csv, os, time
from data_manager import *
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

column = "submisson_time"
desc = False


@app.route('/')
@app.route('/list')
def list_questions():
    global column
    global desc
    order = request.args.get('order')
    if column == order:
        questions = read_questions_correct_format(request.args.get('order'), desc)
        desc = not desc
    else:
        questions = read_questions_correct_format(order)
    
    column = order
    return render_template('questions.html', questions=questions)


@app.route('/question/<int:id>')
def display_question(id):
    answer = read_answers_by_question_id(id)
    question = read_question_by_id(id)
    
    if not question:
        abort(404)
    
    return render_template("answers.html", answer=answer, question=question)


@app.route('/add-question')
@app.route('/add-question', methods=['POST'])
def question_form():
    if request.method == 'POST':
        current_questions = read_questions()
        new_row = dict()
        new_row.update({
            'title'         : request.form.get('title'),
            'message'       : request.form.get('message'),
            'id'            : len(current_questions),
            'submisson_time': format(time.time(), '.0f'),
            'view_number'   : 0,
            'vote_number'   : 0,
            'image'         : ''
        })
        write_question(new_row)
        return redirect(url_for('list_questions'))
    
    return render_template('add-question.html', h1='Create question')


@app.route('/question/<int:question_id>/new-answer')
@app.route('/question/<int:question_id>/new-answer', methods=['POST'])
def answer_form(question_id):
    if request.method == 'POST':
        current_answers = read_answers()
        new_row = dict()
        filename = ''
        file = None
        
        if request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.getcwd() + os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_row.update({
            'id'            : len(current_answers),
            'submisson_time': format(time.time(), '.0f'),
            'vote_number'   : 0,
            'question_id'   : question_id,
            'message'       : request.form.get('message'),
            'image'         : UPLOAD_FOLDER + filename if file else ''
        })
        write_answer(new_row)
        return redirect('/question/{}'.format(question_id))
    
    return render_template('new-answer.html', h1='Create answer')


@app.route('/question/<question_id>/edit')
@app.route('/question/<question_id>/edit', methods=['POST'])
def edit_question(question_id):
    current_questions = read_questions()
    question = []
    index = -1
    
    for i, row in enumerate(current_questions):
        if row['id'] == question_id:
            question = row
            index = i
            break
    
    if request.method == 'POST':
        try:
            question['title'] = request.form.get('title', '')
            question['message'] = request.form.get('message', '')
            question['submisson_time'] = format(time.time(), '.0f')
            
            current_questions.pop(index)
            
            delete_questions()
            
            for row in current_questions:
                write_question(row)
            
            write_question(question)
            
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
    update_vote(question_id, answer_id, type)
    return redirect(url_for("display_question", id=question_id))


if __name__ == '__main__':
    app.secret_key = "topsecret"
    answers = read_answers()
    app.run(debug=True, host='0.0.0.0', port=5000)
