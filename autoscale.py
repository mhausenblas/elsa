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

TRAFFIC_INCREASE_THRESHOLD = 6 # difference between previous and current traffic
SCALE_FACTOR = 2  # part of threshold number of instances should be scaled

################################################################################
# Scaling example:
#
# If TRAFFIC_INCREASE_THRESHOLD == 10 and SCALE_FACTOR == 10 and there has been
# a traffic increase of 25, then this means that (because 25 > 10) the number of
# instances will be increased by a factor of int(25/10) == 2, that is doubled.


################################################################################
# Helper
#

def get_config_params(elsa_config):
    stats_file_path = ''
    traffic_increase_threshold = 6
    scale_factor = 2
    if os.path.exists(elsa_config):
        logging.info('Using %s as config file' %(elsa_config))
        lines = tuple(open(elsa_config, 'r'))
        for line in lines:
            l = str(line).strip()
            if l and not l.startswith('#'): # not empty or comment line
                cfg_param = line.split('=')[0].rstrip() # extract config parameter
                if cfg_param == 'stats-file':
                    stats_file_path = line.split('=')[1].strip().translate(None, '"')
                if cfg_param == 'batch-window':
                    batch_window = int(line.split('=')[1].strip())
                if cfg_param == 'traffic-increase-threshold':
                    traffic_increase_threshold = int(line.split('=')[1].strip())
                if cfg_param == 'scale-factor':
                    scale_factor = int(line.split('=')[1].strip())
    else:
        logging.info('No config file provided.')
    logging.debug('[%s]' %(stats_file_path))
    return (stats_file_path, batch_window, traffic_increase_threshold, scale_factor)

def launch_elsa(marathon, stats_file, scale_window):
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
    
    print('ElSA is deployed and running, waiting now 5 sec before starting auto-scale ...')
    time.sleep(5) # allow time to deploy before autoscaling sets in
    
    # kick off traffic monitoring and trigger autoscaling:
    previous_topic_traffic = 0
    while True:
        with open(stats_file, 'r') as elsa_file:
            topic_traffic = int(elsa_file.read())
            topic_traffic_diff = topic_traffic - previous_topic_traffic
            print('Difference in traffic in last period: %d' %(topic_traffic_diff))
            previous_topic_traffic = topic_traffic
            
            current_instance_num = c.get_app('elsa').instances
            
            if topic_traffic_diff > TRAFFIC_INCREASE_THRESHOLD: # we see a surge of traffic above threshold ...
                instance_multiplier = int(topic_traffic_diff / SCALE_FACTOR) # ... increase number of instances
                c.scale_app('elsa', current_instance_num * instance_multiplier)
                print('Increasing number of instances to %d' %(current_instance_num * instance_multiplier))
            elif topic_traffic_diff < 0: # negative, back off exponentially 
                target_instance_num = int(current_instance_num/2)
                if target_instance_num > 1:
                    c.scale_app('elsa', target_instance_num)
                    print('Decreasing number of instances to %d' %(target_instance_num))
                else:
                    c.scale_app('elsa', 1)
                    print('Resetting number of instances to 1')
        time.sleep(scale_window)

################################################################################
# Main script
#
if __name__ == '__main__':
    try:
        marathon = sys.argv[1] # Marathon URL to use
        (stats_file_path, batch_window, traffic_increase_threshold, scale_factor) = get_config_params(sys.argv[2])
        print('Using %s to monitor topic traffic' %(stats_file))
        if traffic_increase_threshold:
            TRAFFIC_INCREASE_THRESHOLD = traffic_increase_threshold
        if scale_factor:
            SCALE_FACTOR = scale_factor
        print('Using traffic increase threshold of %d and scale factor %d' %(TRAFFIC_INCREASE_THRESHOLD, SCALE_FACTOR))
        launch_elsa(marathon, stats_file_path, batch_window)
    except Exception, e:
        print(e)
        print(__doc__)
        sys.exit(2)