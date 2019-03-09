#!/bin/bash

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

if [ ! -f /data/cms-users-ready ]; then
    if [[ -d "/cmsusers" ]]; then
        cmsImportUser -L italy_yaml -c 1 -A /cmsusers
    fi

    if [[ -v CMS_ADMIN_PASS ]]; then
        cmsAddAdmin admin -p "$CMS_ADMIN_PASS"
    fi

    if [[ -v CMS_TEST_USER ]]; then
        cmsAddUser test test test -p test
        cmsAddParticipation test -c 1
    fi
    touch /data/cms-users-ready
fi

cmsResourceService -a 1
