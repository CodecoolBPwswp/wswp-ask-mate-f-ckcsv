import csv
import datetime


def read_csv(filepath):
    try:
        with open(filepath, encoding='utf-8') as csvfile:
            readCSV = csv.DictReader(csvfile, delimiter=',')
            read_list = []
            for row in readCSV:
                read_list.append(row)
    except FileNotFoundError:
        read_list = []
    return read_list


def write_csv(filepath, header, row):
    for k, v in row.items():
        if isinstance(v, str):
            row[k] = v.replace('\r', '').replace('\n', '<br>')
            
    
    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header, delimiter=',')
        writer.writerow(row)


def delete_csv_data(filepath, header):
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header, delimiter=',')
        writer.writeheader()
