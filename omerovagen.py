#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import datetime
import fileinput
from utils import RSYNC_PATH, FORUM_URL, get_version, get_tag_url
from doc_generator import find_pkg, repl_all


def usage():
    print "gen.py version build"
    sys.exit(1)

try:
    version = sys.argv[1]
    build = sys.argv[2]
except:
    usage()

repl = {"@VERSION@": version,
        "@BUILD@": build,
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y")}

major_version, minor_version = get_version(version)

repl["@TAG_URL@"] = get_tag_url("openmicroscopy", version)
repl["@DOC_URL@"] = "http://www.openmicroscopy.org/site/support/omero%s.%s" \
    % (major_version, minor_version)


PREFIX = os.environ.get('PREFIX', 'omero-virtual-applaince')
DOWNLOADS_PATH = '%s/%s/%s/' % (RSYNC_PATH, PREFIX, version)

repl["@ANNOUNCEMENT_URL@"] = os.environ.get('ANNOUNCEMENT_URL', FORUM_URL)

for x, y in (
        ("VM", "artifacts/OMERO.va-@VERSION@-@BUILD@.ova"),
        ):

    find_pkg(repl, DOWNLOADS_PATH, x, y)


for line in fileinput.input(["omerova_downloads.html"]):
    print repl_all(repl, line, check_http=True),
