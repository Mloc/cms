#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Programming contest management system
# Copyright © 2010-2013 Giovanni Mascellani <mascellani@poisson.phc.unipi.it>
# Copyright © 2010-2012 Stefano Maggiolo <s.maggiolo@gmail.com>
# Copyright © 2010-2012 Matteo Boscariol <boscarim@hotmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Random utilities and logging facilities.

"""

import sys
import datetime
import time

import simplejson as json
from random import choice


def random_string(length):
    """Returns a random string of ASCII letters of specified length.

    """
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return "".join(choice(letters) for unused_i in xrange(length))


def encode_json(obj):
    """Encode a dictionary as a JSON string; on failure, returns None.

    obj (object): the object to encode
    return (string): an encoded string

    """
    try:
        return json.dumps(obj)
    except:
        print >> sys.stderr, "Can't encode JSON: %r" % obj
        raise ValueError


def decode_json(string):
    """Decode a JSON string to a dictionary; on failure, raises an
    exception.

    string (string): the Unicode string to decode
    return (object): the decoded object

    """
    try:
        string = string.decode("utf8")
        return json.loads(string)
    except json.JSONDecodeError:
        print >> sys.stderr, "Can't decode JSON: %s" % string
        raise ValueError


class Logger:
    """Utility class for simple logging.

    """
    def __init__(self):
        self.operation = ""

    def log(self, msg, operation=None, severity=None, timestamp=None):
        """Print a log message.

        msg (string): the message to log
        operation (string): a high-level description of the long-term
                            operation that is going on in the service
        severity (string): a constant defined in Logger
        timestamp (float): seconds from epoch

        """
        if severity is None:
            severity = "INFO"
        if timestamp is None:
            timestamp = time.time()
        if operation is None:
            operation = self.operation

        _datetime = datetime.datetime.fromtimestamp(timestamp)

        if operation == "":
            fmt_string = "%s - %s [%s] - %s"
            print fmt_string % ("{0:%Y/%m/%d %H:%M:%S}".format(_datetime),
                                severity, operation, msg)
        else:
            fmt_string = "%s - %s - %s"
            print fmt_string % ("{0:%Y/%m/%d %H:%M:%S}".format(_datetime),
                                severity, msg)

    def __getattr__(self, method):
        """Syntactic sugar to allow, e.g., logger.debug(...).

        """
        severities = {
            "debug":    "DEBUG   ",
            "info":     "INFO    ",
            "warning":  "WARNING ",
            "error":    "ERROR   ",
            "critical": "CRITICAL"
            }
        if method in severities:
            def new_method(msg, operation=None, timestamp=None):
                """Syntactic sugar around log().

                """
                return self.log(msg, operation, severities[method], timestamp)
            return new_method
