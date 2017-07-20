import os
import sys
import logging
import logging.handlers

def iotlogger(loggername, log_path):
    """
    Function to return logger object
    provoding streaming logs (on your terminal) and
    also logging it to the file
    Parameters
    ----------
    loggername: str
        the name that you want to use for your logger
        (generally the class name)
    logpath: str
        path where you want to save your logs to
    """
    LOG_FNAME = os.path.join(os.path.abspath(log_path), loggername)
    logger = logging.getLogger(loggername)
    # Generic logging level set to DEBUG
    logger.setLevel(logging.DEBUG)
    # format will look something like:
    # [Time] [loggername] [type of log] (module.file.functionName) : (lineNo) -- Message
    formatter = logging.Formatter("%(asctime)s [%(name)8s] [%(levelname)7s] \
    (%(module)s.%(filename)s.%(funcName)s) : %(lineno)s -- %(message)s" ,
                                  datefmt="%d-%m-%Y %H:%M:%S")

    # Log File Handler
    f_handler = logging.handlers.TimedRotatingFileHandler(
        LOG_FNAME, when="midnight", interval=1, backupCount=5)
    f_handler.setFormatter(formatter)
    # Only log info level or higher to the file
    f_handler.setLevel(logging.INFO)
    # To reduce Disk I/O, keep 2000 entries in the memory and then flush
    # it to the file. if you dont want this, comment the below line
    # and at the end of the function, where we add the handler, replace
    # logger.addhandler(memoryHandler) by logger.addhandler(f_handler)
    memoryHandler = logging.handlers.MemoryHandler(capacity=2000, target=f_handler)

    # Log Stream Handler
    s_handler = logging.StreamHandler(stream=sys.stdout)
    s_handler.setFormatter(formatter)
    # Stream debug level logs or higher on the terminal
    s_handler.setLevel(logging.DEBUG)

    logger.addHandler(s_handler)
    logger.addHandler(memoryHandler)
    return logger
