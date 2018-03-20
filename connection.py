import csv


def read_csv(filepath):
    try:
        with open(filepath) as csvfile:
            readCSV = csv.DictReader(csvfile, delimiter=',')
            read_list = []
            for row in readCSV:
                read_list.append(row)
    except FileNotFoundError:
        read_list = []
    return read_list


def write_csv(filepath, header, export_list):
    with open(filepath, 'w') as story_file:
        writer = csv.DictWriter(story_file, fieldnames=header, delimiter=',')
        writer.writeheader()
        for row in export_list:
            writer.writerow(row)
