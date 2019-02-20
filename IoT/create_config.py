import argparse
import os
# -- fix for mac only
#import crypto
import sys
#sys.modules['Crypto'] = crypto
# --
import shutil
from Crypto.PublicKey import RSA
from datetime import datetime

if __name__ == "__main__":

    config_file = "installer-config.txt"
    destination = "files/root/home/pi/.ssh/"
    KEY_DIR = os.getenv('iot_key_dir')

    parser = argparse.ArgumentParser()
    parser.add_argument('-hosts', action='store', dest='total_nodes',
                        help='total number of nodes for which the configuration needs to be generated')
    parser.add_argument('-net', action='store', dest='network',
                        help='Network e.g. 192.168.1.0. Subnet is assumed to be /24')
    parser.add_argument('-st', action='store', dest='start_from',
                        help='start the host naming from. The nodes will be numbered sequentially')
    results = parser.parse_args()

    all_hosts = list(range(int(results.start_from), int(results.start_from)+int(results.total_nodes)))
    _all_ips  = results.network.rstrip('0')+"{host}"
    all_ips  = list(map(lambda x: _all_ips.format(host=x),
                        sorted(all_hosts, reverse=True)))

    for host in all_hosts:
        file_path = os.path.join('{current_host}'.format(current_host=host),
                            destination)
        installer_path = os.path.join('{current_host}'.format(current_host=host))
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
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        print(file_path)
        with open(os.path.join(file_path, 'private.key'), 'wb') as pvtkey_file:
            pvtkey_file.write(key.exportKey('PEM'))
            os.chmod(os.path.join(file_path, 'private.key'), 0o400)
        # change this in config file as well
        if conf.get('user_ssh_pubkey', None):
            conf['user_ssh_pubkey'] = key.publickey().exportKey('OpenSSH').decode('utf-8')
        shutil.copytree(str(host), os.path.join(KEY_DIR, str(host)))
        if conf.get('ip_addr', None):
            conf['ip_addr'] = '.'.join(conf['ip_addr'].split('.')[:-1]) + '.{}'.format(host)
        # write the configuration to a file
        with open(os.path.join(installer_path, 'installer-config.txt'), 'w') as cfg:
            for item in conf.items():
                cfg.write("{key}={value}\n".format(key=item[0], value=item[1]))

        # -- Thats It!
        print("[{time}]: Done configuration for {host}".format(
            time=datetime.now(),
            host=host))
