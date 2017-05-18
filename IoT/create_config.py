import argparse
import os
# -- fix for mac only
import crypto
import sys
sys.modules['Crypto'] = crypto
# --
from Crypto.PublicKey import RSA
from datetime import datetime

if __name__ == "__main__":

    config_file = "./setup/raspberrypi-ua-netinst-v1.5.1/raspberrypi-ua-netinst/config/installer-config.txt"

    parser = argparse.ArgumentParser()
    parser.add_argument('-hosts', action='store', dest='total_nodes',
                        help='total number of nodes for which the configuration needs to be generated')
    parser.add_argument('-net', action='store', dest='network',
                        help='Network e.g. 192.168.1.0. Subnet is assumed to be /24')
    results = parser.parse_args()

    all_hosts = list(range(int(results.total_nodes)))
    _all_ips  = results.network.rstrip('0')+"{host}"
    all_ips  = list(map(lambda x: _all_ips.format(host=x), all_hosts))

    for host in all_hosts:
        path = './{current_host}'.format(current_host=host)
        # parse the config file to a dictionary
        conf = {}
        with open(config_file) as fh:
            for line in fh:
                (key, value) = line.strip('\n').split('=')
                conf[str(key)] = value

        # Values to be changed
        # ip address
        if conf.get('ip_addr', None):
            conf['ip_addr'] = all_ips.pop()
        else:
            print("ERROR: cannot find ip_addr field")

        # ssh public/pvt key
        # generate 2048bit key
        key = RSA.generate(2048)
        # write private key to the file
        os.mkdir(path)
        with open(os.path.join(path, 'private.key'), 'w') as pvtkey_file:
            pvtkey_file.write(key.exportKey('PEM'))
            os.chmod(os.path.join(path, 'private.key'), 0600)
        # change this in config file as well
        if conf.get('user_ssh_pubkey', None):
            conf['user_ssh_pubkey'] = key.publickey().exportKey('OpenSSH')

        # write the configuration to a file
        with open(os.path.join(path, 'installer-config.txt'), 'w') as cfg:
            for item in conf.items():
                cfg.write("{key}={value}\n".format(key=item[0], value=item[1]))
        print("[{time}]: Done configuration for {host}".format(
            time=datetime.now(),
            host=host))
