#!/usr/bin/env python

import csv
import sys

if __name__ == '__main__':
    columns = 0
    datafile = sys.argv[1]
    with open(datafile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for row in csv_reader:
            if columns != len(row):
                columns = len(row)
                print("Columns {0}: {1}".format(columns, row[0])