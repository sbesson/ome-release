#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import datetime
import fileinput

from doc_generator import find_pkg, repl_all


def usage():
    print "figuregen.py version"
    sys.exit(1)

try:
    version = sys.argv[1]
except:
    usage()

repl = {"@VERSION@": version,
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y")}

RSYNC_PATH = os.environ.get('RSYNC_PATH', '/ome/data_repo/public/')
PREFIX = os.environ.get('PREFIX', 'figure')
FIGURE_RSYNC_PATH = '%s/%s/%s/' % (RSYNC_PATH, PREFIX, version)

forum_url = "https://www.openmicroscopy.org/community/viewforum.php?f=11"
repl["@ANNOUNCEMENT_URL@"] = os.environ.get('ANNOUNCEMENT_URL', forum_url)

for x, y in (
        ("FIGURE", "figure-@VERSION@.zip"),
        ):

    find_pkg(repl, FIGURE_RSYNC_PATH, x, y)


for line in fileinput.input(["figure_downloads.html"]):
    print repl_all(repl, line, check_http=True),
