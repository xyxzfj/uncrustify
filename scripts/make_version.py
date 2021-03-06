#!/usr/bin/env python
#
# Rebuilds the version using git describe
#
import sys
import os
import subprocess

def main (argv):
    root = os.path.abspath(os.path.dirname(__file__))
    git_path = os.path.join(root, '.git')
    hg_path = os.path.join(root, '.hg')

    if os.path.exists(git_path):
        try:
            txt = subprocess.check_output(['git', 'describe', '--long', '--always', '--dirty']).strip()
        except:
            print "Failed to retrieve version from git"
            return 1
    elif os.path.exists(hg_path):
        try:
            subprocess.check_call(['hg', 'gexport'])
            node = subprocess.check_output(['hg', '--config', 'defaults.log=', 'log', '-r', '.', '--template', '{gitnode}']).strip()
            txt = subprocess.check_output(['git', '--git-dir=.hg/git', 'describe', '--long', '--tags', '--always', node]).strip()
        except:
            print "Failed to retrieve version from hg"
            return 1
    else:
        print "Unknown version control system."
        return 1

    # convert the git describe text to a version
    pts = txt.split('-', 2)
    full_vers = '%s.%s' % (pts[1], pts[2])
    tag_vers = pts[1]
    print 'full version:', full_vers
    print ' tag version:', tag_vers

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
