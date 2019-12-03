
import os
os.system("cp -r pyonelab tmp_dist")
os.system("rm -rf tmp_dist/bin/*")

# platforms=["Linux","Darwin","Windows"]

platforms=["Linux"]
for p in platforms:
    os.system("cp -r tmp_dist pyonelab-{0}".format(p))
    os.system("cp -r pyonelab/bin/{0} pyonelab-{0}/bin/{0}".format(p))

os.system("rm -rf tmp_dist")
