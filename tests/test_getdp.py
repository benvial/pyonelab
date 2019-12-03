# test for getdp
import subprocess
from pyonelab import getdp


def test_getdp():
    print(getdp)
    out = subprocess.call([getdp, "--info"])
    assert out == 0
