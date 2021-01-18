from __future__ import print_function, division
 
####################################################################
######          Copyright (c)  2015-2020 PGSQL            ##########
####################################################################


import os, sys, json


MY_HOME = os.getenv("MY_HOME", "")
scripts_path = os.path.join(MY_HOME, 'hub', 'scripts')
scripts_lib_path = os.path.join(MY_HOME, 'hub', 'scripts', 'lib')

if scripts_path not in sys.path:
  sys.path.append(scripts_path)
if scripts_lib_path not in sys.path:
  sys.path.append(scripts_lib_path)

import util, startup

pgver = "pg9X"

homedir = os.path.join(MY_HOME, pgver)

datadir = util.get_column('datadir', pgver)

pidfile = os.path.join(datadir, "postmaster.pid")

isJson = os.getenv("isJson", None)

if os.path.isfile(pidfile):
  with open(pidfile, 'r') as f:
    pid = f.readline().rstrip(os.linesep)
else:
  print(pgver + " stopped")
  sys.exit(0)

msg = pgver + " stopping"
if isJson:
  jsonMsg = {}
  jsonMsg['status'] = "wip"
  jsonMsg['component'] = pgver
  jsonMsg['msg'] = msg
  print(json.dumps([jsonMsg]))
else:
  print(msg)

pg_ctl = os.path.join(homedir, "bin", "pg_ctl")

stop_cmd = pg_ctl + ' stop -s -w -m immediate -D "' + datadir + '"'

autostart = util.get_column('autostart', pgver)
if autostart == "on":
  rc = startup.stop_linux("postgresql" + pgver[2:4])
else:
  rc = util.system(stop_cmd)

if (rc > 0):
  msg = "problem stopping " + pgver
  if isJson:
    jsonMsg = {}
    jsonMsg['status'] = "error"
    jsonMsg['component'] = pgver
    jsonMsg['msg'] = msg
    print(json.dumps([jsonMsg]))
  else:
    print(msg)

sys.exit(rc)
