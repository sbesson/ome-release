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
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y"),
        "@YEAR@": datetime.datetime.now().strftime("%Y")}

major_version, minor_version = get_version(version)

repl["@TAG_URL@"] = get_tag_url("openmicroscopy", version)
repl["@DOC_URL@"] = "http://www.openmicroscopy.org/site/support/omero%s.%s" \
    % (major_version, minor_version)
repl["@HELP_URL@"] = "http://help.openmicroscopy.org/getting-started-%s.html"\
    % major_version


PREFIX = os.environ.get('PREFIX', 'omero')
DOWNLOADS_PATH = '%s/%s/%s/' % (RSYNC_PATH, PREFIX, version)

repl["@ANNOUNCEMENT_URL@"] = os.environ.get('ANNOUNCEMENT_URL', FORUM_URL)
repl["@MILESTONE@"] = os.environ.get('MILESTONE', "OMERO-%s" % version)

for x, y in (
        ("LINUX_INSIGHT",
         "artifacts/OMERO.insight-@VERSION@-ice35-@BUILD@-linux.zip"),
        ("MAC_INSIGHT",
         "artifacts/OMERO.insight-@VERSION@-ice35-@BUILD@-mac.zip"),
        ("WIN_INSIGHT",
         "artifacts/OMERO.insight-@VERSION@-ice35-@BUILD@-win.zip"),
        ("IJ_CLIENTS",
         "artifacts/OMERO.insight-ij-@VERSION@-ice35-@BUILD@.zip"),
        ("MATLAB_CLIENTS",
         "artifacts/OMERO.matlab-@VERSION@-ice35-@BUILD@.zip"),
        ("SERVER35", "artifacts/OMERO.server-@VERSION@-ice35-@BUILD@.zip"),
        ("SERVER36", "artifacts/OMERO.server-@VERSION@-ice36-@BUILD@.zip"),
        ("PYTHON35", "artifacts/OMERO.py-@VERSION@-ice35-@BUILD@.zip"),
        ("PYTHON36", "artifacts/OMERO.py-@VERSION@-ice36-@BUILD@.zip"),
        ("JAVA35", "artifacts/OMERO.java-@VERSION@-ice35-@BUILD@.zip"),
        ("JAVA36", "artifacts/OMERO.java-@VERSION@-ice36-@BUILD@.zip"),
        ("DOCS", "artifacts/OMERO.docs-@VERSION@-ice35-@BUILD@.zip"),
        ("SOURCE_CODE", "artifacts/openmicroscopy-@VERSION@.zip"),
        ):

    find_pkg(repl, DOWNLOADS_PATH, x, y)


for line in fileinput.input(["omero_downloads.html"]):
    print repl_all(repl, line, check_http=True),
