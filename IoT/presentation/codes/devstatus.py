import re
import psutil
import misc
import socket
import datetime
import pytz
from mylogger import iotlogger

logger = iotlogger(loggername="DevStatus")

def handle_exception(function):
    def wrapper_function(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            logger.error("Error with " + str(function.func_name) + ":" + str(e), exc_info=True)
            return {}
    return wrapper_function

@handle_exception
def cpuStats():
    logger.debug('Obtaining cpustats')
    cpu_stats = {'cpu_cur_freq': str(psutil.cpu_freq().current).replace('L', ''),
                 'cpu_load': psutil.cpu_percent(percpu=False),
    }
    return cpu_stats

@handle_exception
def memoryStats():
    logger.debug('Obtaining memstats')
    mem = psutil.virtual_memory()
    mem_available = str(mem.available).replace('L', '')
    mem_used = str(mem.used).replace('L', '')
    mem_total = str(mem.total).replace('L', '')
    mem_percent = mem.percent
    mem_stats = {'mem_available': mem_available,
                 'mem_used': mem_used,
                 'mem_total': mem_total,
                 'mem_percent': mem_percent}
    return mem_stats

@handle_exception
def networkStats():
    logger.debug('Obtaining netstats')
    nics = {}
    for nic, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            try:
                socket.inet_aton(addr.address)
                nics.update({"net_"+str(nic): addr.address})
            except Exception as ex:
                # Dont bother, it just means ip address is ipv6
                # or invalid
                pass
    recd_bytes = str(psutil.net_io_counters().bytes_recv).replace('L', '')
    tx_bytes = str(psutil.net_io_counters().bytes_sent).replace('L', '')

    network_stats = {
        'net_rx_packets': recd_bytes,
        'net_tx_packets': tx_bytes,
    }
    network_stats.update(nics)
    return network_stats

@handle_exception
def storageStats():
    logger.debug('Obtaining storagestats')
    root_usage = psutil.disk_usage("/").percent
    storage_stats = {'storage_root': root_usage}
    return storage_stats

def stats():
    timestamp = '{}'.format(datetime.datetime.utcnow().replace(tzinfo = pytz.timezone('America/New_York')))
    cpu_stats = cpuStats()
    mem_stats = memoryStats()
    network_stats = networkStats()
    storage_stats = storageStats()
    status_ping = {}
    status_ping.update(cpu_stats)
    status_ping.update(mem_stats)
    status_ping.update(network_stats)
    status_ping.update(storage_stats)
    status_ping.update({'timestamp': timestamp})
    return status_ping
