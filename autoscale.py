#!/usr/bin/env python
"""
Launches ElSA app using Marathon and scales it depending of topic traffic.

Usage: 
     
    ./autoscale.py $MARATHON_URL

Example: 
     
    ./autoscale.py http://localhost:8080


@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2015-03-06
@status: init
"""

import logging
import sys
import time

from marathon import MarathonClient
from marathon.models import MarathonApp

################################################################################
# Defaults
#

DEBUG = True

if DEBUG:
  FORMAT = '%(asctime)-0s %(levelname)s %(message)s [at line %(lineno)d]'
  logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%dT%I:%M:%S')
else:
  FORMAT = '%(asctime)-0s %(message)s'
  logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt='%Y-%m-%dT%I:%M:%S')

################################################################################
# Helper
#

def get_stats_file(elsa_config):
    stats_file_path = ''
    if os.path.exists(elsa_config):
        logging.info('Using %s as config file' %(elsa_config))
        lines = tuple(open(elsa_config, 'r'))
        for line in lines:
            l = str(line).strip()
            if l and not l.startswith('#'): # not empty or comment line
                cfg_param = line.split('=')[0].rstrip() # extract config parameter
                stats_file_path = line.split('=')[1].strip()
    else:
        logging.info('No config file provided.')
    stats_file_path

def launch_elsa(marathon, stats_file):
    c = MarathonClient(marathon)
    c.create_app('elsa', MarathonApp(cmd='/home/vagrant/elsa/launch-elsa.sh', mem=200, cpus=1, user='vagrant'))
    c.list_apps()

################################################################################
# Main script
#
if __name__ == '__main__':
    try:
        marathon = sys.argv[1] # Marathon URL to use
        stats_file = get_stats_file(sys.argv[2]) # ElSA config file to use
        launch_elsa(marathon, stats_file)
    except Exception, e:
        print(__doc__)
        sys.exit(2)