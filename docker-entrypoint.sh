#!/bin/sh

set -e

if [ ! -f /data/cms-db-ready ]; then
    echo "initialising CMS DB"
    cmsInitDB
    touch /data/cms-db-ready
fi

if [ ! -f /data/cms-contest-ready ]; then
    echo "initialising CMS contest"
    cmsImportContest -i -L italy_yaml /contest
    touch /data/cms-contest-ready
fi

cmsResourceService -a ALL
