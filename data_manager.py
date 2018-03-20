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