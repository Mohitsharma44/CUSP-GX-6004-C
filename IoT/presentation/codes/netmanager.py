import re
import misc
from mylogger import iotlogger

logger = iotlogger(loggername="NetManager")

def iface_params():
    """
    Parameters for Lan
    """
    return [
        '\s*[0-9]+:\s+(?P<device>[a-zA-Z0-9]+).*',
        '.*mtu (?P<mtu>.*).*',
        '.*(inet )(?P<inet>[0-9\.]+).*',
        '.*(inet6 )(?P<inet6>[^/]*).*',
        '.*(inet )[^/]+(?P<netmask>[/][0-9]+).*',
        '.*(ether )(?P<mac>[^\s]*).*',
        '.*inet\s.*(brd )(?P<broadcast>[^\s]*).*',
        '.*inet\s.*(peer )(?P<tun_gw>[^\s]*).*',
    ]

def parameters(interface):
    """
    Get properties for a particular interface
    Parameters
    ----------
    interface: str
        name of the interface to get properties of
        check `get_iface()`
    """
    params = findall(command="ip address show {iface}".format(
        iface=interface), patterns=iface_params())
    return params

def findall(command, patterns):
    """
    Perform re.match against all the patterns
    after running the bash command
    Parameters
    ----------
    command: str
        bash command to execute on system
    patterns: list
        list of patterns to match against
    Returns
    -------
    Returns dictionary
    containing the group name (as passed in pattern element)
    and value as the matched value
    """
    out, error = misc.execute(command.split(" "))
    if error:
        return {}
    else:
        params = {}
        for line in out.splitlines():
            for pattern in patterns:
                match = re.match(pattern, line)
                if match:
                    params.update(match.groupdict())
    return params

def getIP(ifacename):
    """
    Returns IP address of the interface
    `ifacename`
    Parameters
    ----------
    ifacename: str
        interface name. e.g. "wlan0"
    Returns
    -------
    ip_address: str
        ip address for `ifacename`
    """
    try:
        return parameters(ifacename).get('inet', '')
    except Exception as ex:
        logger.error("Error getting ip address: " + str(ex))

def getMac(ifacename):
    """
    Returns MAC address of the interface
    `ifacename`
    Prameters
    ---------
    ifacename: str
        interface name. e.g. "wlan0"
    Returns
    -------
    mac_address: str
        mac address for `ifacename`
    """
    try:
        return parameters(ifacename).get('mac', '')
    except Exception as ex:
        logger.error("Error getting Mac address "+str(ex))
