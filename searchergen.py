#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import datetime
import fileinput

from doc_generator import find_pkg, repl_all

fingerprint_url = "http://ci.openmicroscopy.org/fingerprint"
MD5s = []


def usage():
    print "searchergen.py version pyslidversion ricercaversion"
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

RSYNC_PATH = os.environ.get('RSYNC_PATH', '/ome/data_repo/public/')
PREFIX = os.environ.get('PREFIX', 'searcher')
SEARCHER_RSYNC_PATH = '%s/%s/%s/' % (RSYNC_PATH, PREFIX, version)

forum_url = "https://www.openmicroscopy.org/community/viewforum.php?f=11"
repl["@ANNOUCEMENT_URL@"] = os.environ.get('ANNOUCEMENT_URL', forum_url)

for x, y in (
        ("SEARCHER", "artifacts/omero_searcher-@VERSION@-b@BUILDNUM@.tar.gz"),
        ("PYSLID", "artifacts/pyslid-@PYSLIDVERSION@-b@BUILDNUM@.tar.gz"),
        ("RICERCA", "artifacts/ricerca-@RICERCAVERSION@-b@BUILDNUM@.tar.gz"),
        ):

    find_pkg(repl, fingerprint_url, SEARCHER_RSYNC_PATH, x, y, MD5s)


for line in fileinput.input(["searcher_downloads.html"]):
    print repl_all(repl, line, check_http=True),
