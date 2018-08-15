import json
import csv

def export_json_to_csv(json_data, file_name):
    with open(json_data, 'r') as read_file:
        data = json.load(read_file)

    # open a file for writing

    file = open('storage/reports/' + file_name , 'w')

    # create the csv writer object

    csvwriter = csv.writer(file)

    count = 0

    for item in data:
        if count == 0:
            header = item.keys()
            csvwriter.writerow(header)
            count += 1
        csvwriter.writerow(item.values())

    file.close()