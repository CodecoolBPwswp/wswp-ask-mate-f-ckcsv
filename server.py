import os
from werkzeug.utils import secure_filename
from user import *

import sql_data_manager

UPLOAD_FOLDER = sql_data_manager.UPLOAD_FOLDER
app = Flask(__name__)
app.secret_key = "234o23uiféojvweőirg39fuü2müdfővpk"
app.register_blueprint(user_page)

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
        sql_data_manager.add_comment(id, request.form["answer_id"], request.form["message"], session["user_id"])
        return redirect(url_for("display_question", id=id) + "#" + request.form["answer_id"])

    sql_data_manager.count_view(id)

    return render_template("answers.html", answer=answer, question=question, answer_comments=answer_comments)


@app.route('/add-question')
@app.route('/add-question', methods=['POST'])
def question_form():
    if request.method == 'POST':
        sql_data_manager.write_question(request.form.get('title'), request.form.get('message'), session["user_id"])
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
                file.save(os.getcwd() + os.path.join(UPLOAD_FOLDER, filename))
        
        message = request.form.get('message')
        image = UPLOAD_FOLDER + filename if file else ''
        
        sql_data_manager.write_answer(question_id, message, image, session["user_id"])
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
    return redirect(url_for("display_question", id=question_id) + "#v_" + answer_id)


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    answer_ids = sql_data_manager.get_answer_ids_by_question_id(question_id)
    for answer_id in answer_ids:
        delete_answer(answer_id.get('id'))
    sql_data_manager.delete_question(question_id)
    return redirect(url_for("list_questions"))


@app.route('/delete_answer/<answer_id>', methods=['POST'])
def delete_answer(answer_id):
    image_path = sql_data_manager.get_image_name_by_answer_id(answer_id)
    if UPLOAD_FOLDER in image_path:
        os.remove(os.getcwd() + image_path.get('image'))
    question_id = sql_data_manager.delete_answer(answer_id)
    return redirect(url_for("display_question", id=question_id))


def highlight(text: str, term: str):
    text = text.replace(
            term.title(), "<mark>" + term.title().strip() + "</mark>"
    ).replace(
            term.lower(), "<mark>" + term.lower() + "</mark>"
    ).replace(
            term.upper(), "<mark>" + term.upper() + "</mark>"
    )
    return text


@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('search_term', None)
    search_term = search_term.lower()
    
    if not search_term:
        return redirect(url_for('list_questions'))

    questions = sql_data_manager.search_questions(search_term)
    answers = sql_data_manager.search_answers(search_term)

    for question in questions:
        question['title'] = highlight(question['title'], search_term)
        question['message'] = highlight(question['message'], search_term)
    
    for answer in answers:
        answer['message'] = highlight(answer['message'], search_term)

    print(answers)

    return render_template('search.html', questions=questions, answers=answers)


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


@app.route('/comment/<comment_id>/delete')
def delete_comment(comment_id):

    question_id = sql_data_manager.read_question_id_by_comment_id(comment_id)[0]['question_id']

    sql_data_manager.delete_comment(comment_id)

    return redirect('/question/{}'.format(question_id))


@app.route('/comment/<comment_id>/edit')
@app.route('/comment/<comment_id>/edit', methods=['POST'])
def edit_comment(comment_id):

    comment_to_edit = int(comment_id)
    question_id = sql_data_manager.read_question_id_by_comment_id(comment_id)[0]['question_id']

    if request.method == 'POST':
        sql_data_manager.edit_comment(18, request.form["message"])
        return redirect(url_for("display_question", id=question_id))

    return redirect(url_for("display_question", id=question_id, comment_to_edit=comment_to_edit))


@app.route('/list-users')
def list_users():

    user_list = sql_data_manager.list_users()

    return render_template('list_users.html', user_list=user_list)


@app.route('/user/<user_id>')
def user_page(user_id):

    username = sql_data_manager.list_users(user_id)[0]['username']

    user_questions = sql_data_manager.user_questions(user_id)

    user_answers = sql_data_manager.user_answers(user_id)

    user_comments = sql_data_manager.user_comments(user_id)

    return render_template('user_page.html', user_questions=user_questions,
                           user_answers=user_answers, user_comments=user_comments, username=username)


@app.route('/<int:question_id>/new-tag')
@app.route('/<int:question_id>/new-tag', methods=['POST'])
def new_tag():

    if request.method == 'POST':
        sql_data_manager.new_tag(request.form.get("tag"), )

    return render_template('new_tag.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
