#!/bin/bash

#Remember to run this script with sudo!
HOSTS=2
ROUTERS=4
CHANNELS=2

HEADER='hosts+routers+channels+cost'

MEASUREMENTS_DIR='measurements'
 CHANGING_ROUTERS_NO_FILE=$MEASUREMENTS_DIR/changing_routers_no.csv

 echo $HEADER > $CHANGING_ROUTERS_NO_FILE
 for ROUTERS in $(seq 2 20)
 do
     ./clearNetbox.sh
     echo \n\n\n\n\nGenerating topology:
     echo \ndragonfly_topology.py --setup --hosts=$HOSTS --routers=$ROUTERS --channels=$CHANNELS
     python3 dragonfly_topology.py --setup --hosts=$HOSTS --routers=$ROUTERS --channels=$CHANNELS
     COST=`python3 dragonfly_topology.py --costs`
     echo ${HOSTS}+${ROUTERS}+${CHANNELS}+${COST} >> $CHANGING_ROUTERS_NO_FILE
 done


CHANGING_CHANNELS_NO_FILE=$MEASUREMENTS_DIR/changing_channels_no.csv
ROUTERS=5

echo $HEADER > $CHANGING_CHANNELS_NO_FILE
for CHANNELS in $(seq 1 10)
do
    ./clearNetbox.sh
    echo \n\n\n\n\nGenerating topology:
    echo \ndragonfly_topology.py --setup --hosts=$HOSTS --routers=$ROUTERS --channels=$CHANNELS
    python3 dragonfly_topology.py --setup --hosts=$HOSTS --routers=$ROUTERS --channels=$CHANNELS
    COST=`python3 dragonfly_topology.py --costs`
    echo ${HOSTS}+${ROUTERS}+${CHANNELS}+${COST} >> $CHANGING_CHANNELS_NO_FILE
done