#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*- 
"""
run script for testing lib

"""

import urllib3
import xmltodict
import logging
import sys
import os
import time, datetime
import paramiko
import yaml
import subprocess


__location__ = sys.argv[0]
__directory__ = os.path.dirname(__location__)
__config__ = os.path.join(__directory__, 'config')
__lib__ = os.path.join(__directory__, 'lib')
sys.path.append(__lib__)

from git_handler import WorkCopy


if __name__ == '__main__':
    from optparse import OptionParser
    args_options = OptionParser()
    args_options.add_option("-a", "--app", dest="app", help="application name")
    args_options.add_option("-l", "--lbranch", dest="lbranch", help="local branch name")
    args_options.add_option("-r", "--rbranch", dest="rbranch", help="remote branch name")
    (options, args) = args_options.parse_args()
    if options.app is None or options.lbranch is None or options.rbranch is None:
        print >> sys.stderr, "At least one required option is missing"
        sys.exit(1)

    repository_list={}    
    with open(os.path.join(__config__, "git_projects.yaml")) as git_progects:
        projects = yaml.load(git_progects.read())
    for (key, val)  in projects.items():
        repository_list[key]=val
    wc=WorkCopy(options.app, repository_list[options.app], options.lbranch, "./wc", "regular")
    wc.mergesquash(options.rbranch)
