import os
from connection import *

QUESTION_FILE_PATH = os.getenv('QUESTION_FILE_PATH') if 'QUESTION_FILE_PATH' in os.environ else 'question.csv'
QUESTION_HEADER = ['id', 'submisson_time', 'view_number', 'vote_number', 'title', 'message', 'image']

ANSWER_FILE_PATH = os.getenv('ANSWER_FILE_PATH') if 'ANSWER_FILE_PATH' in os.environ else 'answer.csv'
ANSWER_HEADER = ['id', 'submisson_time', 'vote_number', 'question_id', 'message', 'image']


def read_questions():
    return read_csv(QUESTION_FILE_PATH)


def write_questions(export_list):
    write_csv(QUESTION_FILE_PATH, QUESTION_HEADER, export_list)


def read_answers():
    return read_csv(ANSWER_FILE_PATH)


def write_answers(export_list):
    write_csv(ANSWER_FILE_PATH, ANSWER_HEADER, export_list)


def read_answers_by_question_id(question_id):
    answers = read_answers()
    match = []

    for answer in answers:
        if answer["id"] == question_id:
            match.append(answer)

    return match


def read_question_by_id(id):
    questions = read_questions()

    for question in questions:
        if question["id"] == id:
            return question

    return []