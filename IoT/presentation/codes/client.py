import json
import pycurl
import cStringIO
import devstatus
from mylogger import iotlogger

logger = iotlogger(loggername="Uploader")

def getStatus():
    """
    Obtain device status from `devstatus`
    Returns
    -------
    status_ping
        json dump of dictionary contatining status
        of the device
    """
    try:
        return devstatus.stats()
    except Exception as ex:
        logger.error("Could not obtain Device Status: "+str(ex))

def uploadStatus(status, server="http://localhost:8888/status_upload"):
    """
    Upload Status
    Parameters
    ----------
    status: json dump
        json.dumps(<status_str / dict>)
    server: str
        full uri of the server location to upload to
    """
    logger.debug("Uploading Status")
    c = pycurl.Curl()
    response = cStringIO.StringIO()
    c.setopt(pycurl.URL, "http://localhost:8888/status_upload")
    c.setopt(pycurl.TIMEOUT, 5)
    c.setopt(
        pycurl.HTTPHEADER, [
            'id: ' + 'ajd629'])
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.POSTFIELDS, status)
    c.setopt(pycurl.WRITEFUNCTION, response.write)
    c.perform()
    if response.getvalue() == 'OK':
        logger.info('Uploaded Device Status')
