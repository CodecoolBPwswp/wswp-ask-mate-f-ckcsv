import database_common
import bcrypt

UPLOAD_FOLDER = '/static/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


@database_common.connection_handler
def read_questions(cursor, order, ascdesc):
    cursor.execute("""
        SELECT * FROM question
        ORDER BY {} {}
    """.format(order, ascdesc))
    
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
def read_answer_by_id(cursor, id):
    cursor.execute("""
        SELECT * FROM answer WHERE id = %(id)s
    """, {'id': id})
    
    answer = cursor.fetchall()
    
    return answer


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
def update_answer(cursor, id, message):
    message = message.replace('\r', '').replace('\n', '<br>')
    cursor.execute(
            """
            UPDATE answer SET submisson_time = localtimestamp(0), message = %(message)s
            WHERE id=%(id)s
            """, {'id': id, 'message': message}
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
            SELECT question_id FROM answer WHERE id=%(id)s
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
def read_question_id_by_answer_id(cursor, answer_id):
    cursor.execute("""
        SELECT question_id FROM answer WHERE id = %(answer_id)s
    """, {'answer_id': answer_id})
    
    question_id = cursor.fetchall()
    
    return question_id


@database_common.connection_handler
def read_question_id_by_comment_id(cursor, comment_id):
    cursor.execute("""
        SELECT question_id FROM comment WHERE id = %(comment_id)s
    """, {'comment_id': comment_id})

    question_id = cursor.fetchall()

    return question_id


@database_common.connection_handler
def search_questions(cursor, search_term):
    cursor.execute(
            """
            SELECT * FROM question
            WHERE LOWER(title) LIKE %(search_term)s OR LOWER(message) LIKE %(search_term)s
            ORDER BY submisson_time DESC
            """, {'search_term': ('%' + search_term + '%')}
    )
    
    questions = cursor.fetchall()
    
    return questions


@database_common.connection_handler
def search_answers(cursor, search_term):
    cursor.execute(
            """
            SELECT message, question_id FROM answer
            WHERE LOWER(message) LIKE %(search_term)s
            ORDER BY submisson_time DESC
            """, {'search_term': ('%' + search_term + '%')}
    )
    
    answers = cursor.fetchall()
    
    return answers


@database_common.connection_handler
def answer_comments(cursor, question_id):
    cursor.execute("""
                    SELECT id, answer_id, message FROM comment
                    WHERE question_id = %(question_id)s   
                """, {'question_id': question_id})
    
    comments = cursor.fetchall()
    
    return comments


@database_common.connection_handler
def add_comment(cursor, question_id, answer_id, message):
    cursor.execute("""
                    INSERT INTO comment (question_id, answer_id, message,  submission_time)
                    VALUES (%(question_id)s, %(answer_id)s, %(message)s, localtimestamp(0))
                    """, {"question_id": question_id, "answer_id": answer_id, "message": message})


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@database_common.connection_handler
def delete_comment(cursor, id):
    cursor.execute("""
                   DELETE FROM comment
                   WHERE id = %(id)s
                    """, {'id':id})


@database_common.connection_handler
def edit_comment(cursor, id, message):
    cursor.execute("""
                   UPDATE comment SET message = %(message)s, submission_time = localtimestamp(0)
                   WHERE id = %(id)s
                    """, {'id':id, 'message':message})


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@database_common.connection_handler
def registration(cursor, username, password):
    hash_pass = hash_password(password)

    cursor.execute("""
                    INSERT INTO "user" (username, password) VALUES(%(username)s, %(password)s) RETURNING *; 
                    """, {"username": username, "password": hash_pass})

    data = cursor.fetchone()

    return data

@database_common.connection_handler
def check_if_user_exists(cursor, username):

    cursor.execute("""
                    SELECT * FROM "user"
                    WHERE username=%(username)s
                    """, {"username": username})

    data = cursor.fetchone()

    return data
