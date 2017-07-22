import os
import subprocess
from mylogger import iotlogger

logger = iotlogger(loggername="misc")

def execute(command=None, std_in=subprocess.PIPE,
            std_out=subprocess.PIPE, std_err=subprocess.PIPE):
    """
    Execute shell commands

    Parameters
    ----------
    command: list
        command string should be split at every space
        and be passed as a list
    Returns
    -------
    out: str
        string output of the command
    err: bool
        True if error was raised in executing the command
    """
    logger.debug("Executing: "+" ".join(command))
    out = err = False
    try:
        proc = subprocess.Popen([cmd for cmd in command],
                                stdin=std_in,
                                stdout=std_out,
                                stderr=std_err)
        out, err = proc.communicate()
    except Exception as ex:
        logger.error("Error executing: "+" ".join(command)+ " "+ str(ex))
        err = True
    finally:
        return out, err
