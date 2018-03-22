import os, shutil
from connection import *

QUESTION_FILE_PATH = os.getenv('QUESTION_FILE_PATH') if 'QUESTION_FILE_PATH' in os.environ else 'question.csv'
QUESTION_HEADER = ['id', 'submisson_time', 'view_number', 'vote_number', 'title', 'message', 'image']

ANSWER_FILE_PATH = os.getenv('ANSWER_FILE_PATH') if 'ANSWER_FILE_PATH' in os.environ else 'answer.csv'
ANSWER_HEADER = ['id', 'submisson_time', 'vote_number', 'question_id', 'message', 'image']


def read_questions_correct_format(ordered_by):
    question_list = read_csv(QUESTION_FILE_PATH)
    for question in question_list:
        question["submisson_time"] = datetime.datetime.fromtimestamp(int(question["submisson_time"])).strftime(
                '%Y-%m-%d %H:%M:%S')

    if not ordered_by:
        ordered(question_list, "submisson_time")
    else:
        ordered(question_list, ordered_by)
    return question_list


def read_questions():
    question_list = read_csv(QUESTION_FILE_PATH)
    return question_list


def write_question(export_data):
    write_csv(QUESTION_FILE_PATH, QUESTION_HEADER, export_data)


def read_answers():
    return read_csv(ANSWER_FILE_PATH)


def write_answer(export_data):
    write_csv(ANSWER_FILE_PATH, ANSWER_HEADER, export_data)


def read_answers_by_question_id(question_id):
    answers = read_answers_correct_format()
    match = []
    
    for answer in answers:
        if int(answer["question_id"]) == question_id:
            match.append(answer)
    
    return match


def read_question_by_id(id):
    questions = read_questions_correct_format()
    
    for question in questions:
        if int(question["id"]) == id:
            return question
    
    return []


def ordered(question_list, key, desc=True):
    return question_list.sort(key=lambda x: x[key], reverse=desc)


def delete_questions():
    delete_csv_data(QUESTION_FILE_PATH, QUESTION_HEADER)


def update_vote(question_id, answer_id, type):
    answers = read_answers()

    delete_csv_data(ANSWER_FILE_PATH, ANSWER_HEADER)

    for answer in answers:
        if answer["id"] == answer_id and int(answer["question_id"]) == question_id:

            if type == "vote-up":
                answer["vote_number"] = str(int(answer["vote_number"]) + 1)
            else:
                answer["vote_number"] = str(int(answer["vote_number"]) - 1)

        write_answer(answer)


def read_answers_correct_format(ordered_by=None):
    if not ordered_by:
        ordered_by = "submisson_time"
    answer_list = read_csv(ANSWER_FILE_PATH)
    for answer in answer_list:
        answer["submisson_time"] = datetime.datetime.fromtimestamp(int(answer["submisson_time"])).strftime(
                '%Y-%m-%d %H:%M:%S')
        ordered(answer_list, ordered_by )
    return answer_list