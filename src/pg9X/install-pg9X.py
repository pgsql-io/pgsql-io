
import util
import os, sys

pgver="pg9X"
thisDir = os.path.dirname(os.path.realpath(__file__))

isAutoStart = str(os.getenv("isAutoStart", "False"))
isFIPS = str(os.getenv("isFIPS", "False"))

if isFIPS == "True":
  util.message("Configuring for FIPS")
  os.system("rm -v " + thisDir + "/lib/libcrypt*")
  os.system("rm -v " + thisDir + "/lib/libssl*")

if isAutoStart != "True":
  sys.exit(0)

#########################################################
## AutoStart 
#########################################################
svcuser = util.get_user()

util.message("Initializing " + str(pgver) + " as a service to run as " + str(svcuser))
script = thisDir + os.sep + "init-" + pgver + ".py --svcuser=" + str(svcuser)
cmd = sys.executable + " -u " + script
rc = os.system(cmd)

util.message("Configuring " + str(pgver) + " to Autostart")
script = thisDir + os.sep + "config-" + pgver + ".py --autostart=on"
cmd = sys.executable + " -u " + script
rc = os.system(cmd)

util.tune_postgresql_conf(pgver)

util.message("Starting " + str(pgver) + " for first time")
script = thisDir + os.sep + "start-" + pgver + ".py"
cmd = sys.executable + " -u " + script
rc = os.system(cmd)

# This script runs after the install script succeeds and must
# therefore always has to return "success"
sys.exit(0)

