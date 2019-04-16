#!/usr/bin/env python


"""dns-map

Parse the DNS logs  
 
Usage:
  dns-map.py -h | --help
  dns-map.py (-d <FILENAME> )
   
Options:
  -h --help                      Show this screen.
  -d --datafile=<FILENAME>       Data file to parse
  --loglevel=<LEVEL>                  Log level
"""

import struct 
import re
from docopt import docopt
import logging
import csv
from collections import defaultdict

def parse_data(csv_file):
    col_timestamp = 0
    col_org_id = 1
    col_policy = 5
    col_domain = 29
    orgs = defaultdict(lambda: defaultdict(int))
    csv_reader = csv.reader(csv_file, delimiter='\t')
    for row in csv_reader:
        policy = row[col_policy]
        if policy == "Abuse": continue;
        org_id = row[col_org_id]
        domain_name = row[col_domain]
        orgs[org_id][domain_name] += 1 

if __name__ == '__main__':
    try:
        arguments = docopt(__doc__, version='dns-map')

        logging.basicConfig()    
        logger = logging.getLogger('dns-map')
        loglevel = arguments['--loglevel']
        if loglevel is None:
            loglevel = "DEBUG"
        logger.setLevel(getLevelName(loglevel))
    
        datafile = arguments['--datafile']
        if datafile is None:
            logger.error("I am missing a --datafile command line argument")
            exit(1)
            
        with open(datafile) as csv_file:
            parse_data(csv_file)
    
    except Exception as e:
        print e        
