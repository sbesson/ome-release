#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import datetime
import fileinput
import re
import github

from doc_generator import find_pkg, repl_all


def usage():
    print "gen.py version build [build_ice34]"
    sys.exit(1)

try:
    version = sys.argv[1]
    build = sys.argv[2]
except:
    usage()

repl = {"@VERSION@": version,
        "@BUILD@": build,
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y")}

# Read major and minor version from input version
split_version = re.split("^([0-9]+)\.([0-9]+)\.([0-9]+)(.*?)$", version)
major_version = int(split_version[1])
minor_version = int(split_version[2])

# For calculating tags
gh = github.Github()
ome = "openmicroscopy"
scc = "snoopycrimecop"

repo1 = gh.get_organization(ome).get_repo(ome)
repo2 = gh.get_user(scc).get_repo(ome)

for repo in (repo1, repo2):
    found = False
    for tag in repo.get_tags():
        if tag.name == ("v%s" % version):
            found = True
            break
    if found:
        break

repl["@TAG_URL@"] = repo.html_url + '/tree/' + tag.name
repl["@DOC_URL@"] = "http://www.openmicroscopy.org/site/support/omero%s.%s" \
    % (major_version, minor_version)
repl["@HELP_URL@"] = "http://help.openmicroscopy.org/getting-started-%s.html"\
    % major_version

RSYNC_PATH = os.environ.get('RSYNC_PATH', '/ome/data_repo/public/')
PREFIX = os.environ.get('PREFIX', 'omero')
OMERO_RSYNC_PATH = '%s/%s/%s/' % (RSYNC_PATH, PREFIX, version)

forum_url = "https://www.openmicroscopy.org/community/viewforum.php?f=11"
repl["@ANNOUNCEMENT_URL@"] = os.environ.get('ANNOUNCEMENT_URL', forum_url)
repl["@MILESTONE@"] = os.environ.get('MILESTONE', "OMERO-%s" % version)

for x, y in (
        ("LINUX_INSIGHT",
         "artifacts/OMERO.insight-@VERSION@-ice35-@BUILD@.linux.zip"),
        ("MAC_JAVA6_INSIGHT",
         "artifacts/OMERO.insight-@VERSION@-ice35-@BUILD@.mac_Java6.zip"),
        ("MAC_JAVA7+_INSIGHT",
         "artifacts/OMERO.insight-@VERSION@-ice35-@BUILD@.mac_Java7+.zip"),
        ("WIN_INSIGHT",
         "artifacts/OMERO.insight-@VERSION@-ice35-@BUILD@.win.zip"),
        ("IJ_CLIENTS",
         "artifacts/OMERO.insight-ij-@VERSION@-ice35-@BUILD@.zip"),
        ("MATLAB_CLIENTS",
         "artifacts/OMERO.matlab-@VERSION@-ice35-@BUILD@.zip"),
        ("SERVER34", "artifacts/OMERO.server-@VERSION@-ice34-@BUILD@.zip"),
        ("SERVER35", "artifacts/OMERO.server-@VERSION@-ice35-@BUILD@.zip"),
        ("PYTHON34", "artifacts/OMERO.py-@VERSION@-ice34-@BUILD@.zip"),
        ("PYTHON35", "artifacts/OMERO.py-@VERSION@-ice35-@BUILD@.zip"),
        ("JAVA35", "artifacts/OMERO.java-@VERSION@-ice35-@BUILD@.zip"),
        ("DOCS", "artifacts/OMERO.docs-@VERSION@-ice34-@BUILD@.zip"),
        ("VM", "artifacts/OMERO.vm-@VERSION@-@BUILD@.ova"),
        ("DOC", "artifacts/OMERO-@VERSION@.pdf"),
        ("SOURCE_CODE", "artifacts/openmicroscopy-@VERSION@.zip"),
        ):

    find_pkg(repl, OMERO_RSYNC_PATH, x, y)


for line in fileinput.input(["omero_downloads.html"]):
    print repl_all(repl, line, check_http=True),
