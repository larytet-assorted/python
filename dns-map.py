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
        
    
    except Exception as e:
        print e        
