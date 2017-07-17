import os
from datetime import datetime
from functools import partial
from subprocess import Popen, PIPE
import multiprocessing as mp

# absolute path for raspberry-ua-netinst
source_dir = 'setup/raspberrypi-ua-netinst-v1.5.1'

# additional files from dir
source_dir2 = './'

# absolute path for the memcard formatted in MsDOS format
drives = [
    '/Volumes/0',
    '/Volumes/1',
    '/Volumes/2',
    '/Volumes/3'
]

destination2 = [
    '/Volumes/0/raspberrypi-ua-netinst/config',
    '/Volumes/1/raspberrypi-ua-netinst/config',
    '/Volumes/2/raspberrypi-ua-netinst/config',
    '/Volumes/3/raspberrypi-ua-netinst/config',
]

# all the hosts to be written to at the same time
hosts = [
    78,
    79,
    80,
    81
]

def copy(source, destination):
    print("[{time}]: Copying to {dest}".format(time=datetime.now(),
                                               dest=destination))
    proc = Popen("rsync" + " -r " + source + "/ " + destination,
                 shell=True, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()

if __name__ == "__main__":
    pool = mp.Pool(4)
    results  = [pool.apply_async(copy, args=(source_dir, drive))
                for drive in drives]

    results2 = [pool.apply_async(copy,
                           args=(os.path.join(os.path.abspath(source_dir2),
                                              str(hosts[i])),
                                 destination2[i]))
                for i in range(len(destination2))]
    pool.close()
    pool.join()
    print("[{time}]: Done!".format(time=datetime.now()))
