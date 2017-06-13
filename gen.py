#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import datetime
import fileinput
import json

from utils import RSYNC_PATH, FORUM_URL, get_version, get_tag_json
from doc_generator import find_artifact, repl_all


def usage():
    print "gen.py version build"
    sys.exit(1)


try:
    version = sys.argv[1]
    build = sys.argv[2]
except:
    usage()


d = {}
d['component'] = 'bio-formats'
d['version'] = version
d['buildnumber'] = build
d['year'] = datetime.datetime.now().strftime("%Y")
d.update(get_tag_json("openmicroscopy", version))

# Read major and minor version from input version
major_version, minor_version = get_version(version)

repl = {
    "@VERSION@": d['version'],
    "@BUILD@": d['buildnumber'],
    "@YEAR@": d['year'],
    "@TAG_URL@": d['url'],
    "@DOC_URL@": "https://docs.openmicroscopy.org/%s/%s" % (
        d['component'], d['version']),
    "@HELP_URL@": "http://help.openmicroscopy.org/getting-started-%s.html" % (
        major_version)
    }

PREFIX = os.environ.get('PREFIX', 'omero')
DOWNLOADS_PATH = '%s/%s/%s/' % (RSYNC_PATH, PREFIX, version)

repl["@ANNOUNCEMENT_URL@"] = os.environ.get('ANNOUNCEMENT_URL', FORUM_URL)
repl["@MILESTONE@"] = os.environ.get('MILESTONE', "OMERO-%s" % version)

artifacts = {
    "LINUX_INSIGHT": "artifacts/OMERO.insight-%s-ice36-%s-linux.zip" % (
        d['version'], d['buildnumber']),
    "MAC_INSIGHT": "artifacts/OMERO.insight-%s-ice36-%s-mac.zip" % (
        d['version'], d['buildnumber']),
    "WIN_INSIGHT": "artifacts/OMERO.insight-%s-ice36-%s-win.zip" % (
        d['version'], d['buildnumber']),
    "IJ_CLIENTS": "artifacts/OMERO.insight-ij-%s-ice36-%s.zip" % (
        d['version'], d['buildnumber']),
    "MATLAB_CLIENTS": "artifacts/OMERO.matlab-%s-ice36-%s.zip" % (
        d['version'], d['buildnumber']),
    "SERVER36": "artifacts/OMERO.server-%s-ice36-%s.zip" % (
        d['version'], d['buildnumber']),
    "PYTHON36": "artifacts/OMERO.py-%s-ice36-%s.zip" % (
        d['version'], d['buildnumber']),
    "JAVA36": "artifacts/OMERO.java-%s-ice36-%s.zip" % (
        d['version'], d['buildnumber']),
    "DOCS": "artifacts/OMERO.apidoc-%s-ice36-%s.zip" % (
        d['version'], d['buildnumber']),
    "DOC": "artifacts/OMERO.doc-%s.zip" % d['version'],
    "SOURCE_CODE": "artifacts/openmicroscopy-%s.zip" % d['version'],
    }

d['artifacts'] = []
for (k, v) in artifacts.iteritems():
    artifact = find_artifact(DOWNLOADS_PATH, v)
    d['artifacts'].append(artifact)
    repl["@%s@" % k] = "./" + artifact['path']
    repl["@%s_MD5@" % k] = artifact['md5'][0:8]
    repl["@%s_SHA1@" % k] = artifact['sha1'][0:8]
    repl["@%s_SIZE@" % k] = artifact['humansize']
    repl["@%s_BASE@" % k] = os.path.basename(artifact['path'])


with open('index.json', 'w') as outfile:
    json.dump(d, outfile)

with open('index.html', 'w') as outfile:
    for line in fileinput.input(["omero_downloads.html"]):
        outfile.write(repl_all(repl, line, check_http=True))
