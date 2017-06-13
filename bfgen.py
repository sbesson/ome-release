#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import fileinput
import json

from utils import RSYNC_PATH, get_version, get_tag_json
from doc_generator import find_artifact, repl_all


def usage():
    print "bfgen.py version"
    sys.exit(1)


try:
    version = sys.argv[1]
except:
    usage()

d = {}
d['component'] = 'bio-formats'
d['version'] = version
d['year'] = datetime.datetime.now().strftime("%Y")
d.update(get_tag_json("bioformats", version))

PREFIX = os.environ.get('PREFIX', 'bio-formats')
BF_RSYNC_PATH = '%s/%s/%s/' % (RSYNC_PATH, PREFIX, version)


# Create replacement dictionary
repl = {
    "@VERSION@": d['version'],
    "@YEAR@": d['year'],
    "@TAG_URL@": d['url'],
    "@DOC_URL@": "https://docs.openmicroscopy.org/%s/%s" % (
        d['component'], d['version'])
    }

artifacts = {
    'COMMAND_LINE_TOOLS': "artifacts/bftools.zip",
    'MATLAB_TOOLS': "artifacts/bfmatlab.zip",
    'OCTAVE_PACKAGE': "artifacts/bioformats-octave-%s.tar.gz" % version,
    "DOC": "artifacts/bio-formats-doc-%s.zip" % version,
    "JAVADOCS": "artifacts/bio-formats-javadocs-%s.zip" % version,
    "SOURCE_CODE_ZIP": "artifacts/bioformats-%s.zip" % version,
    "SOURCE_CODE_TXZ": "artifacts/bioformats-%s.tar.xz" % version,
    "bioformats_package.jar": "artifacts/bioformats_package.jar",
    "bio-formats_plugins.jar": "artifacts/bio-formats_plugins.jar",
    "bio-formats-testing-framework.jar":
        "artifacts/bio-formats-testing-framework.jar",
    "formats-api.jar": "artifacts/formats-api.jar",
    "formats-bsd.jar": "artifacts/formats-bsd.jar",
    "formats-gpl.jar": "artifacts/formats-gpl.jar",
    "jai_imageio.jar": "artifacts/jai_imageio.jar",
    "loci_tools.jar": "artifacts/loci_tools.jar",
    "turbojpeg.jar": "artifacts/turbojpeg.jar",
}


d['artifacts'] = []
for (k, v) in artifacts.iteritems():
    artifact = find_artifact(BF_RSYNC_PATH, v)
    d['artifacts'].append(artifact)
    repl["@%s@" % k] = "./" + artifact['path']
    repl["@%s_MD5@" % k] = artifact['md5'][0:8]
    repl["@%s_SHA1@" % k] = artifact['sha1'][0:8]
    repl["@%s_SIZE@" % k] = artifact['humansize']
    repl["@%s_BASE@" % k] = os.path.basename(artifact['path'])


with open('index.json', 'w') as outfile:
    json.dump(d, outfile)

with open('index.html', 'w') as outfile:
    for line in fileinput.input(["bf_downloads.html"]):
        outfile.write(repl_all(repl, line, check_http=True))
