import csv
import os

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'data.csv'
DATA_HEADER = ['id', 'title', 'user_story', 'acceptance_criteria', 'business_value', 'estimation', 'status']


def get_all_user_story():
    try:
        with open(DATA_FILE_PATH) as csvfile:
            readCSV = csv.DictReader(csvfile, delimiter=';')
            user_stories = []
            for row in readCSV:
                user_stories.append(row)
    except FileNotFoundError:
        user_stories = []
    return user_stories


def write_csv(export_list):
    with open(DATA_FILE_PATH, 'w') as story_file:
        writer = csv.DictWriter(story_file, fieldnames=DATA_HEADER, delimiter=';')
        writer.writeheader()
        for row in export_list:
            writer.writerow(row)
