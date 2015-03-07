#!/usr/bin/env python
"""
Launches ElSA app using Marathon and scales it depending of topic traffic.

Usage: 
     
    ./autoscale.py $MARATHON_URL $ELSA_CONFIG_FILE

Example: 
     
    ./autoscale.py http://localhost:8080 ./elsa.conf


@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2015-03-06
@status: init
"""

import logging
import os
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
                if cfg_param == 'stats-file':
                    stats_file_path = line.split('=')[1].strip()
    else:
        logging.info('No config file provided.')
    logging.debug('[%s]' %(stats_file_path))
    return stats_file_path

def launch_elsa(marathon, stats_file):
    logging.info('Start monitoring the inbound traffic on topics using %s' %(stats_file))
    # make sure the stats file is created:
    if not os.path.exists(stats_file):
        open(stats_file, 'w').close()
    
    c = MarathonClient(marathon)
    c.create_app('elsa', MarathonApp(cmd='/home/vagrant/elsa/launch-elsa.sh', mem=200, cpus=1, user='vagrant'))
    # c.list_apps()

    previous_topic_traffic = 0
    while True:
        with open (stats_file, 'r') as elsa_file:
            topic_traffic = int(elsa_file.read())
            print('Difference in traffic since last period: %d' %(topic_traffic - previous_topic_traffic))
            previous_topic_traffic = topic_traffic
        sleep(6) # TBD: read 'batch-window' from conf and make slightly higher, hard coded for now

################################################################################
# Main script
#
if __name__ == '__main__':
    try:
        marathon = sys.argv[1] # Marathon URL to use
        stats_file = get_stats_file(sys.argv[2]) # ElSA config file to use
        print('Using %s to monitor topic traffic' %(stats_file))
        launch_elsa(marathon, stats_file)
    except Exception, e:
        print(__doc__)
        sys.exit(2)