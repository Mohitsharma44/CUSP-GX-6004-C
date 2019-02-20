`create_config.py` -- helper script for prepping the Pi with dynamically generated ssh keys, IP addresses

Creates configuration for `n` hosts using `installer-config.txt` config file as template. It modifies the `ssh-pub-key` and `ip_addr` based on the host parameter. The generated ssh key and configuration file are stored in the directory with name as the last octet of the host's IP address.
Once the ssh file is created, it is also copied of the `server` directory so that it can be served to the students.

Example:
- parameters:

``` bash
python create_config.py --help

usage: create_config.py [-h] [-hosts TOTAL_NODES] [-net NETWORK]
                        [-st START_FROM]

optional arguments:
  -h, --help          show this help message and exit
  -hosts TOTAL_NODES  total number of nodes for which the configuration needs
                      to be generated
  -net NETWORK        Network e.g. 192.168.1.0. Subnet is assumed to be /24
  -st START_FROM      start the host naming from. The nodes will be numbered
                      sequentially
```

- To create 10 hosts with ip address starting from 192.168.1.50 - 192.168.1.60:
`python create_config.py -hosts 10 -net 192.168.1.0 -st 50`


`flash_image.py` -- Multiprocess-helper script for copying the installer file from [`setup`](./setup) directory, generated configuration file from above using rsync
