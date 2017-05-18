import os
import asyncio
from subprocess import Popen, PIPE
from datetime import datetime

# absolute path for raspberry-ua-netinst
source_dir = 'setup/raspberrypi-ua-netinst-v1.5.1'

# additional files from dir
source_dir2 = ''

# absolute path for the memcard formatted in MsDOS format
drives = [
    '/Volumes/0',
    '/Volumes/1',
    '/Volumes/2',
    '/Volumes/3'
]

# all the hosts to be written to at the same time
hosts = [
    50,
    51,
    52,
    53
]

@asyncio.coroutine
def copy(source, destination):
    print("[{time}]: Copying to {dest}".format(time=datetime.now(),
                                               dest=destination))
    proc = Popen("rsync" + " -r " + source + "/ " + destination,
                 shell=True, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()

if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    results = [copy(source_dir, drive) for drive in drives]
    results = results + [copy(os.path.join(source_dir2, str(hosts[i])),
                              drive) for i, drive in enumerate(drives)]
    event_loop.run_until_complete(asyncio.wait(results))
    print("[{time}]: Done!".format(time=datetime.now()))
