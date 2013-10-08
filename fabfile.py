from fabric.api import *
import fabric.contrib.project as project
import os

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path

# Remote server configuration
production = 'root@localhost:22'
dest_path = '/var/www'

# Rackspace Cloud Files configuration settings
env.cloudfiles_username = 'my_rackspace_username'
env.cloudfiles_api_key = 'my_rackspace_api_key'
env.cloudfiles_container = 'my_cloudfiles_container'

def clean():
    if os.path.isdir(DEPLOY_PATH):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir -p {deploy_path}'.format(**env))
    if os.path.isdir('content'):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir -p {deploy_path}'.format(**env))

def omero(tag, build):
    clean()
    local("mkdir -p content")
    local('python gen.py %s %s > content/index.md' % (tag, build))
    build()

def bf(tag, build):
    clean()
    local("mkdir -p content")
    local('python gen.py %s %s > content/index.md' % (tag, build))
    build()

def build():
    local('pelican -s pelicanconf.py content')

def rebuild():
    clean()
    build()

def regenerate():
    local('pelican -r -s pelicanconf.py content')

def serve():
    local('cd {deploy_path} && python -m SimpleHTTPServer'.format(**env))

def reserve():
    build()
    serve()
