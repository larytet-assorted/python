#!/usr/bin/env python


"""dns-map

Parse the DNS logs  
 
Usage:
  dns-map.py -h | --help
  dns-map.py (-d <FILENAME> ) [-l <LOGLEVEL>]
   
Options:
  -h --help                      Show this screen.
  -d --datafile=<FILENAME>       Data file to parse
  -l --loglevel=<LEVEL>             Log level
"""

import struct 
import re
from docopt import docopt
import logging
import csv
from collections import defaultdict


def get_top_domain(domain_name, count=3):
    top_domain = ".".join(domain_name.split(".")[-count:])
    return top_domain


ignore_list_3 = {"s.sophosxl.net", "s3.amazonaws.com", "j.e5.sk", "fna.fbcdn.net", "xx.fbcdn.net",  
              "p1.dsvml.net", "v1.dsvml.net", "swy.nhs.uk", "nflxvideo.net",
              "nuid.imrworldwide.com", "metric.gstatic.com", "loris.llnwd.net", "init.cedexis-radar.net", 
              "fls.doubleclick.net", "drip.trouter.io", "nrb.footprintdns.com", "avts.mcafee.com",
              "ap.spotify.com", "aa.online-metrix.net"}

'''
This list reduces number of unique domain names by 60%
'''
ignore_list_2 = {"gstatic.com":0, "sophosxl.net":0, "doubleclick.net":0, "amazonaws.com":0, "e5.sk":0, 
                 "fbcdn.net":0,  
                 "dsvml.net":0, "nhs.uk":0, "nflxvideo.net":0,
                 "imrworldwide.com":0, "llnwd.net":0, "cedexis-radar.net":0, 
                 "trouter.io":0, "footprintdns.com":0, "mcafee.com":0,
                 "spotify.com":0, "online-metrix.net":0, "addr.arpa":0}

def is_ignored(domain_name):
    top_domain = get_top_domain(domain_name, 2)
    res = top_domain in ignore_list_2
    if res:
        ignore_list_2[top_domain] += 1
    return res

def compare_domains(x, y):
    x = get_top_domain(x)
    y = get_top_domain(y)
    if x < y:
        return -1
    elif y < x:
        return 1
    else:
        return 0

def order_by_top_domain(domains):
    if type(domains) is dict:
        domains = domains.values()
    domains.sort(cmp=compare_domains) 
    return domains

def create_compare_domains_count(domains):
    def compare_domains_count(x, y):
        x = domains[x]
        y = domains[y]
        if x < y:
            return 1
        elif y < x:
            return -1
        else:
            return 0
        
    return compare_domains_count

def order_by_count(domains):
    domainsList = domains.keys()
    domainsList.sort(cmp=create_compare_domains_count(domains)) 
    return domainsList

def create_compare_value_len(d):
    def compare_value_len(x, y):
        x = len(d[x])
        y = len(d[y])
        if x < y:
            return 1
        elif y < x:
            return -1
        else:
            return 0
        
    return compare_value_len

def order_by_value_len(orgs):
    orgsList = orgs.keys()
    orgsList.sort(cmp=create_compare_value_len(orgs)) 
    return orgsList
    
def parse_data(csv_file):
    '''
    Processes ~400K lines/s
    '''
    col_timestamp = 0
    col_org_id = 1
    col_policy = 5
    col_domain = 29
    orgs = defaultdict(lambda: defaultdict(int))
    domains = defaultdict(int)
    csv_reader = csv.reader(csv_file, delimiter='\t')
    rows = 0
    ignored_domains = 0
    for row in csv_reader:
        rows += 1
        policy = row[col_policy]
        if policy == "Abuse": continue;
        org_id = row[col_org_id]
        domain_name = row[col_domain]
        if is_ignored(domain_name):
            ignored_domains += 1
            continue
        domains[domain_name] += 1
        orgs[org_id][domain_name] += 1 
    logger.debug("Handled {0} rows, collected {1} orgs, ignored {2} domains".format(rows, len(orgs), ignored_domains))
    return orgs, domains

def get_random_domains(orgs, domains):
    top_domains = defaultdict(int)
    for domain_name, _ in domains.items():
        top_domain = get_top_domain(domain_name) 
        top_domains[top_domain] += 1
        
    random_domains = []
    for domain_name, count in domains.items():
        top_domain = get_top_domain(domain_name) 
        if count < 2 and top_domains[top_domain] > 30:
            random_domains.append(domain_name)
    return random_domains, top_domains

def print_domains(orgs):
    orgs_list = order_by_value_len(orgs)
    for org in orgs_list:
        domain_names = orgs[org]
        print("{0} {1}".format(org, len(domain_names)))
        domain_list = order_by_count(domain_names)
        for domain_name in domain_list:
            count = domain_names[domain_name]
            print("\t{0} {1}".format(domain_name, count))
  
if __name__ == '__main__':
    arguments = docopt(__doc__, version='dns-map')

    logging.basicConfig()    
    logger = logging.getLogger('dns-map')
    loglevel = arguments['--loglevel']
    if loglevel is None:
        loglevel = "DEBUG"
    logger.setLevel(loglevel)
    
    datafile = arguments['--datafile']
    if datafile is None:
        logger.error("I am missing a --datafile command line argument")
        exit(1)
        
    with open(datafile) as csv_file:
        orgs, domains = parse_data(csv_file)
        '''
        random_domains, top_domains = get_random_domains(orgs, domains)
        logger.debug("Collected {0} unique domains, {1} random domains".format(len(domains), len(random_domains)))
        random_domains_sorted = order_by_top_domain(random_domains)
        for k, v in ignore_list_2.iteritems(): 
            print(k, v)
            pass
        '''
        print_domains(orgs)
