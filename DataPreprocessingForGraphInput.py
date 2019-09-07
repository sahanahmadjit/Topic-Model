import csv
from typing import TextIO


with open('/home/C00408440/ZWorkStation/JournalVersion/index_test.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    line_count =0
    for line in csv_reader:
        for term in range(len(line)):
            print(line[term])