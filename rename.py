#!/usr/bin/python

import argparse
import fileinput
import fnmatch
import os

def replace(name, branch, uid):
  for root, dir, files in os.walk("."):
    yml = list(fnmatch.filter(files, "*.yml"))
    xml = list(fnmatch.filter(files, "*.xml"))
    dkr = list(fnmatch.filter(files, "Dockerfile"))
    for f in yml + xml:
      fname = os.path.join(root, f)
      print "Setting space to '%s' in %s" % (name, fname)
      for line in fileinput.input([fname], inplace=True):
        line = line.replace("SPACENAME", name)
        line = line.replace("SPACEBRANCH", name)
        print line,
    for f in dkr:
      fname = os.path.join(root, f)
      for line in fileinput.input([fname], inplace=True):
        line = line.replace("SPACEUSER", str(uid))
        print line,

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--uid", type=int, default=os.getuid())
  parser.add_argument("name")
  parser.add_argument("branch", nargs="?")
  ns = parser.parse_args()
  name = ns.name
  branch = ns.branch
  if not branch:
    branch = name

  replace(name, branch, ns.uid)
  print "Done. You may want to review and commit your changes now"
