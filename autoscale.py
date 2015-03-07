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

TRAFFIC_INCREASE_THRESHOLD = 10 # difference between previous and current traffic
SCALE_FACTOR = 10  # part of threshold number of instances should be scaled

################################################################################
# Scaling example:
#
# If TRAFFIC_INCREASE_THRESHOLD == 10 and SCALE_FACTOR == 10 and there has been
# a traffic increase of 25, then this means that (because 25 > 10) the number of
# instances will be increased by a factor of int(25/10) == 2, that is doubled.


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
                    stats_file_path = line.split('=')[1].strip().translate(None, '"')
    else:
        logging.info('No config file provided.')
    logging.debug('[%s]' %(stats_file_path))
    return stats_file_path

def launch_elsa(marathon, stats_file):
    logging.info('Start monitoring the inbound traffic on topics using %s' %(stats_file))
    # make sure the stats file is properly initialized:
    if not os.path.exists(stats_file):
        f = open(stats_file, 'w')
        f.write('0')
        f.close()
    
    # launch the Elsa app via Marathon
    c = MarathonClient(marathon)
    c.create_app('elsa', MarathonApp(cmd='/home/vagrant/elsa/launch-elsa.sh', mem=200, cpus=1, user='vagrant'))
    # c.list_apps()

    # kick off traffic monitoring:
    previous_topic_traffic = 0
    while True:
        with open(stats_file, 'r') as elsa_file:
            topic_traffic = int(elsa_file.read())
            topic_traffic_diff = topic_traffic - previous_topic_traffic
            print('Difference in traffic since last period: %d' %(topic_traffic_diff))
            previous_topic_traffic = topic_traffic
            
            current_instance_num = c.get_app('elsa').instances
            
            if topic_traffic_diff > TRAFFIC_INCREASE_THRESHOLD: # we see a surge of traffic above threshold ...
                instance_multiplier = int(topic_traffic_diff / SCALE_FACTOR) # ... increase number of instances
                c.scale_app('elsa', current_instance_num * instance_multiplier )
            else if topic_traffic_diff < 0: # negative, back off exponentially 
                target_instance_num = int(current_instance_num/2)
                if target_instance_num > 1:
                    c.scale_app('elsa', target_instance_num)
                else
                    c.scale_app('elsa', 1)
            
        time.sleep(6) # TBD: read 'batch-window' from conf and make slightly higher, hard coded for now

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
        print(e)
        print(__doc__)
        sys.exit(2)