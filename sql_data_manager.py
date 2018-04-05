import database_common

UPLOAD_FOLDER = '/static/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


@database_common.connection_handler
def read_questions(cursor, order="submisson_time", desc=False):
    if order is None:
        order = 'submisson_time'
    
    if not desc:
        cursor.execute("""
            SELECT * FROM question
            ORDER BY {} ASC
        """.format(order))
    else:
        cursor.execute("""
                    SELECT * FROM question
                    ORDER BY {} DESC
                """.format(order))
    
    questions = cursor.fetchall()
    
    return questions


@database_common.connection_handler
def read_question_by_id(cursor, id):
    cursor.execute("""
        SELECT * FROM question WHERE id = %(id)s
    """, {'id': id})
    
    question = cursor.fetchall()
    
    return question


@database_common.connection_handler
def read_answers_by_question_id(cursor, id):
    cursor.execute("""
            SELECT * FROM answer WHERE question_id = %(id)s ORDER BY id ASC
        """, {'id': id})
    
    answer = cursor.fetchall()
    
    return answer


@database_common.connection_handler
def write_question(cursor, title, message):
    message = message.replace('\r', '').replace('\n', '<br>')
    cursor.execute(
            """
            INSERT INTO question (submisson_time, title, message) VALUES (localtimestamp(0),%(title)s,%(message)s)
            """, {'title': title, 'message': message}
    )


@database_common.connection_handler
def write_answer(cursor, question_id, message, image):
    message = message.replace('\r', '').replace('\n', '<br>')
    cursor.execute(
            """
            INSERT INTO answer (submisson_time,question_id, message, image) VALUES (localtimestamp(0),%(question_id)s,
            %(message)s,%(image)s)
            """, {'question_id': question_id, 'message': message, 'image': image}
    )


@database_common.connection_handler
def update_question(cursor, id, title, message):
    message = message.replace('\r', '').replace('\n', '<br>')
    cursor.execute(
            """
            UPDATE question SET submisson_time = localtimestamp(0), title = %(title)s, message = %(message)s
            WHERE id=%(id)s
            """, {'id': id, 'title': title, 'message': message}
    )


@database_common.connection_handler
def update_vote(cursor, answer_id, type):
    step = 1 if type == 'vote-up' else -1
    cursor.execute(
            """
            UPDATE answer SET vote_number = vote_number + ({})
            WHERE id = {}
            """.format(step, answer_id)
    )


@database_common.connection_handler
def delete_question(cursor, id):
    cursor.execute(
            """
            DELETE FROM answer WHERE question_id=%(id)s;
            DELETE FROM question_tag WHERE question_id=%(id)s;
            DELETE FROM comment WHERE question_id=%(id)s;
            DELETE FROM question WHERE id = %(id)s
            """, {'id': id}
    )


@database_common.connection_handler
def delete_answer(cursor, id):
    cursor.execute(
            """
            SELECT question_id from answer WHERE id=%(id)s
            """, {'id': id}
    )
    result = cursor.fetchall()
    question_id = result[0]['question_id']
    cursor.execute(
            """
            DELETE FROM comment WHERE answer_id=%(id)s;
            DELETE FROM answer WHERE id=%(id)s;
            """, {'id': id}
    )
    return question_id


@database_common.connection_handler
def search_questions(cursor, search_term, order="submisson_time", desc=False):
    if order is None:
        order = 'submisson_time'
    
    if not desc:
        cursor.execute("""
            SELECT * FROM question
            WHERE title LIKE '%{search_term}%' OR message LIKE '%{search_term}%'
            ORDER BY {order} ASC
        """.format(order=order, search_term=search_term))
    else:
        cursor.execute("""
                    SELECT * FROM question
                    ORDER BY {} DESC
                """.format(order))
    
    questions = cursor.fetchall()
    
    return questions


@database_common.connection_handler
def answer_comments(cursor, question_id):
    cursor.execute("""
                    SELECT answer_id, message FROM comment
                    WHERE question_id = %(question_id)s   
                """, {'question_id': question_id})

    comments = cursor.fetchall()

    return comments

@database_common.connection_handler
def add_comment(cursor, question_id, answer_id, message, submission_time):
    cursor.execute("""
                    INSERT INTO comment (question_id, answer_id, message, submission_time) 
                    VALUES (%(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s)
                    """, {"question_id": question_id, "answer_id": answer_id, "message": message, "submission_time": submission_time})
