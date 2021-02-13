########################################################
#  Copyright 2020-2021  OpenRDS   All rights reserved. #
########################################################

import sys, os

VER="7.00"
REPO=os.getenv("REPO", "https://openrds-download.s3.amazonaws.com/REPO")
  
if sys.version_info < (3, 4):
  print("ERROR: Requires Python 3.4 or greater")
  sys.exit(1)

from urllib import request as urllib2
import tarfile

IS_64BITS = sys.maxsize > 2**32
if not IS_64BITS:
  print("ERROR: This is a 32-bit machine and our packages are 64-bit.")
  sys.exit(1)

if os.path.exists("openrds"):
  print("ERROR: Cannot install over an existing 'openrds' directory.")
  sys.exit(1)

my_file="openrds-io-" + VER + ".tar.bz2"
f = REPO + "/" + my_file

if not os.path.exists(my_file):
  print("Downloading OpenRDS CLI " + VER + " ...")
  try:
    fu = urllib2.urlopen(f)
    local_file = open(my_file, "wb")
    local_file.write(fu.read())
    local_file.close()
  except Exception as e:
    print("ERROR: Unable to download " + f + "\n" + str(e))
    sys.exit(1)

print("Unpacking ...")
try:
  tar = tarfile.open(my_file)
  tar.extractall(path=".")
  tar.close()
  os.remove(my_file)
except Exception as e:
  print("ERROR: Unable to unpack \n" + str(e))
  sys.exit(1)

cmd = "openrds" + os.sep + "io"
os.system(cmd + " set GLOBAL REPO " + REPO)

print("OpenRDS CLI installed.\n")

sys.exit(0)

