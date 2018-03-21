import csv
import datetime


def read_csv(filepath):
    try:
        with open(filepath) as csvfile:
            readCSV = csv.DictReader(csvfile, delimiter=',')
            read_list = []
            for row in readCSV:
                row["submisson_time"] = datetime.datetime.fromtimestamp(int(row["submisson_time"])).strftime('%Y-%m-%d %H:%M:%S')
                read_list.append(row)
    except FileNotFoundError:
        read_list = []
    return read_list


def write_csv(filepath, header, row):
    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header, delimiter=',')
        writer.writerow(row)