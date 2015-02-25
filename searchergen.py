#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import datetime
import fileinput

from utils import RSYNC_PATH, FORUM_URL
from doc_generator import find_pkg, repl_all


def usage():
    print "searchergen.py version pyslidversion ricercaversion buildnum"
    sys.exit(1)

try:
    version = sys.argv[1]
    pyslidversion = sys.argv[2]
    ricercaversion = sys.argv[3]
    buildnum = sys.argv[4]
except:
    usage()

repl = {"@VERSION@": version,
        "@PYSLIDVERSION@": pyslidversion,
        "@RICERCAVERSION@": ricercaversion,
        "@BUILDNUM@": buildnum,
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y")}

PREFIX = os.environ.get('PREFIX', 'searcher')
SEARCHER_RSYNC_PATH = '%s/%s/%s/' % (RSYNC_PATH, PREFIX, version)

repl["@ANNOUNCEMENT_URL@"] = os.environ.get('ANNOUNCEMENT_URL', FORUM_URL)

for x, y in (
        ("SEARCHER", "artifacts/omero_searcher-@VERSION@-b@BUILDNUM@.tar.gz"),
        ("PYSLID", "artifacts/pyslid-@PYSLIDVERSION@-b@BUILDNUM@.tar.gz"),
        ("RICERCA", "artifacts/ricerca-@RICERCAVERSION@-b@BUILDNUM@.tar.gz"),
        ):

    find_pkg(repl, SEARCHER_RSYNC_PATH, x, y)


for line in fileinput.input(["searcher_downloads.html"]):
    print repl_all(repl, line, check_http=True),
