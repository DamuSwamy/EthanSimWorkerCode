#!/bin/bash


#!/bin/bash

HOST="45.113.38.41"
PORT="990"
USERNAME="Ethan"
PASSWORD='B!ll!ng#$#'
REMOTE_DIRECTORY="/Ethan/"


lftp -u $USERNAME,$PASSWORD ftps://$HOST:$PORT <<EOF
set ssl:verify-certificate no
set ftp:ssl-protect-data true
put output/runrateoutput.csv
exit
EOF
