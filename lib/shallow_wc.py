#!/usr/bin/env python3

import os
import subprocess
import sys

"""
upload a git shallow workcopy

"""

class WorkCopy():
    def __init__(self, app, branch, wc_path):
        self.app = app
        self.branch = branch
        self.wc_path=wc_path
        self.repository="ssh://gerrit/%s" % (app)
        self.work_dir="%s/%s" %(wc_path, app)
        self.load_wc()
       
    def load_wc(self):
        if self.__check_if_wc_exist__():
            self.__exec_git__("checkout -f", self.work_dir)
            self.__exec_git__("clean -fd", self.work_dir)
            self.__exec_git__("checkout %s" % (self.branch), self.work_dir)
            self.__exec_git__("pull --rebase origin %s" % (self.branch), self.work_dir)        
        else:
            self.__exec_git__("clone --single-branch --depth 1 --branch %s %s" %(self.branch, self.repository), self.wc_path)

            
    def delete_wc(self):
        cmd="rm -rf %s" %(self.work_dir)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = proc.stdout.read()
        proc.wait()
        
    def __exec_git__(self, cmd, path):
        try:
            cmd="git %s" %(cmd)
            proc = subprocess.Popen(cmd, cwd=r'%s'%(path), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = proc.communicate()
            if proc.returncode:
                print(proc.returncode)
                raise Exception(error)
        except Exception:
            print(error)

                
    def __check_if_wc_exist__(self):
        if os.path.exists("%s" %(self.work_dir)):
            return True
        else:
            return False
        
            
if __name__ == '__main__':
    from optparse import OptionParser
    args_options = OptionParser()
    args_options.add_option("-a", "--app", dest="app", help="application name")
    args_options.add_option("-b", "--branch", dest="branch", help="ci release version")
    (options, args) = args_options.parse_args()
    if options.app is None or options.branch is None:
        print >> sys.stderr, "At least one required option is missing"
        sys.exit(1)
        
    wc=WorkCopy(options.app, options.branch, "../wc")
    wc.load_wc()
