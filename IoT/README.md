`create_config.py` -- helper script for prepping the Pi with dynamically generated ssh keys, IP addresses

Creates configuration for `n` hosts using `installer-config.txt` config file as template. It modifies the `ssh-pub-key` and `ip_addr` based on the host parameter. The generated ssh key and configuration file are stored in the directory with name as the last octet of the host's IP address.


`flash_image.py` -- Multiprocess-helper script for copying the installer file from [`setup`](./setup) directory, generated configuration file from above using rsync
