#!/bin/bash

PYTHON=/opt/backend/bin/python
UWSGI=/opt/backend/bin/uwsgi
SO=/opt/backend/bin/activate
PP=/opt/backend/project
###
#
#Export app path to PYTHONPATH
#
###
function export_it {

export PYTHONPATH=$PYTHONPATH:$PP


}
###
#
#Start uwsgi in foreground
#
###
function start_it {

$($UWSGI --socket 127.0.0.1:8080 --protocol=http --module version_1 --callable app)

}
###
#
#Start uwsgi in background
#
###

function detach_it {

$($UWSGI --socket 127.0.0.1:8080 --module version_1 --callable app &)

}
###
#
# main function 
#
###
function main {

# source virtual env
$(source $SO)
export_it
detach_it

}
main
