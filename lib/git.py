#!/usr/bin/python

import os
import inspect
import re
from subprocess import Popen, PIPE, STDOUT

class GitCmd:

    def __init__(self, dir, log, BARE = False):
        if BARE:
            self.git_dir = "--git-dir=" + os.path.abspath(dir)
        else:
            self.git_dir = "--git-dir=" + os.path.join(os.path.abspath(dir), ".git")
        self.work_tree = "--work-tree=" + os.path.join(os.path.abspath(dir))
        self.log = log
        self.dir = dir

    def fetch(self, remote, ref):
        self.log.info("Fetching %s from %s", ref, remote)
        commands = ["git", self.git_dir, self.work_tree, inspect.stack()[0][3], remote, ref]
        final_command = " ".join(commands)
        self.__exec__(final_command)

    def checkout(self, branch):
        self.log.info("Switch to %s branch in %s dir", branch, self.git_dir)
        commands = ["git", self.git_dir, self.work_tree, inspect.stack()[0][3], branch]
        final_command = " ".join(commands)
        self.__exec__(final_command)

    def for_each_ref(self, ref):
        cmd = inspect.stack()[0][3].replace("_","-")
        commands = ["git", self.git_dir, cmd, re.escape("--format=%(refname)"), ref+"*"]
        final_command = " ".join(commands)
        o = self.__exec__(final_command)
        list = o.split()
        num_list = []
        for l in list:
            m = re.search(r'\.v(.*)', str(l))
            if m:
                num_list.append(int(m.group(0)[2:]))
        if len(num_list):       
            return max(num_list)
        else:
            return 0

    def get_next_ver(self, branch):
        latest_v = self.for_each_ref("refs/ver/"+branch)
        next_v = latest_v + 1
        self.log.info("Latest version: %s", latest_v)
        self.log.info("Next version: %s", next_v)
        return next_v

    def push_ver_tag(self, branch, version):
        tag = "%s.v%s" % (branch, version)
        self.log.info("Pushing new version %s tag", tag)
        commands = ["git", self.git_dir, "push", "origin", "HEAD:refs/ver/"+tag]
        final_command = " ".join(commands)
        self.__exec__(final_command)

    def update_bare(self):
        self.log.info("Update bare repo")
        commands = ["git", self.git_dir, "fetch", "origin"]
        final_command = " ".join(commands)
        self.__exec__(final_command)

    def update_version(self):
        self.log.info("Update versions in bare repo")
        commands = ["git", self.git_dir, "fetch", "origin", "refs/ver/*:refs/ver/*"]
        final_command = " ".join(commands)
        self.__exec__(final_command)

    def clone_bare(self):
        self.log.info("Clone bare to workspace")
        commands = ["git", "clone", self.dir, self.work_tree]
        final_command = " ".join(commands)
        self.__exec__(final_command)


    def __exec__(self, final_command):
        proc = Popen(final_command, stdout=PIPE, stderr=STDOUT, shell=True)
        output = proc.stdout.read().strip()
        if output:
            print output
        return output
