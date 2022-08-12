## -*- coding: utf-8 -*-
from Tools.logger import log
import subprocess


def runcmd(cmd):
    """Input CMD Command"""
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = process.communicate()
    retcode = process.poll()
    log.info("Input: " + cmd)
    if retcode:
        if len(str(err)[2:-1]) == 0:
            log.error(str(output)[2:-5])
        else:
            log.error(str(err)[2:-5])
        return False
    else:
        outputall = str(output).replace('\\r\\n', '\n')[2:-5]
        if outputall.strip() == "":
            pass
        else:
            log.info('Output: ' + str(output).replace('\\r\\n', '\n')[2:-5])
        return True

if __name__ == '__main__':
    cmd = "adb -s e2da2f5f shell grep xl4.update-report /mnt/ota/data/log/dmclient.log"
    print(runcmd(cmd))