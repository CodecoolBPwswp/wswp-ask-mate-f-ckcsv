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
            SELECT * FROM answer WHERE question_id = %(id)s
        """, {'id': id})

    answer = cursor.fetchall()

    return answer


@database_common.connection_handler
def write_question(cursor, title, message):
    cursor.execute(
        """
        INSERT INTO question (submisson_time, title, message) VALUES (localtimestamp(0),%(title)s,%(message)s)
        """, {'title': title, 'message': message}
    )
