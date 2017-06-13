#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import scc.git

RSYNC_PATH = os.environ.get(
    'RSYNC_PATH', '/ome/www/downloads.openmicroscopy.org')
FORUM_URL = "https://www.openmicroscopy.org/community/viewforum.php?f=11"


def get_version(version):
    """Read major and minor version from input version"""
    version_pattern = re.compile("^([0-9]+)\.([0-9]+)\.([0-9]+)(.*?)$")
    split_version = version_pattern.split(version)
    major_version = int(split_version[1])
    minor_version = int(split_version[2])
    return (major_version, minor_version)


def get_tag(repo_name, version, org="openmicroscopy",
            fork="snoopycrimecop", prefix="v"):
    """Return URL of GitHub tag matching a version"""

    # Retrieve organization and fork repositories
    gh = scc.git.get_github(scc.git.get_token())
    org_repo = gh.get_organization(org).get_repo(repo_name)
    fork_repo = gh.get_user(fork).get_repo(repo_name)

    for repo in (org_repo, fork_repo):
        for tag in repo.get_tags():
            if tag.name == ("%s%s" % (prefix, version)):
                return tag

    return None


def get_tag_url(repo_name, version, org="openmicroscopy",
                fork="snoopycrimecop", prefix="v"):
    """Return URL of GitHub tag matching a version"""

    # Retrieve organization and fork repositories
    json = get_tag_json(repo_name, version, org=org, fork=fork, prefix=prefix)

    return json['url']


def get_tag_json(repo_name, version, org="openmicroscopy",
                 fork="snoopycrimecop", prefix="v"):
    """Return JSON for a GitHub tag"""

    # Retrieve organization and fork repositories
    tag = get_tag(repo_name, version, org=org, fork=fork, prefix=prefix)

    if tag:
        return {'sha': tag.commit.sha, 'url': tag.commit.url}
    else:
        return None
