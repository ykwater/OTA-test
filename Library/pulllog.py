from Tools.cmder import runcmd
from Tools.path import LOG_PATH, TEMP_PATH
from Tools.value import var


btbox = var.V_BTBOX


def pullotalog(id, tbox):
    if tbox == "H97-A":
        cmd1 = f"adb -s {btbox} shell tar -cvf /mnt/ota/data/{id}log.tar /mnt/ota/data/log"
        cmd2 = f"adb -s {btbox} pull /mnt/ota/data/{id}log.tar {LOG_PATH}/otalog"
    elif tbox == "H97-B":
        cmd1 = f"adb -s {btbox} shell tar -cvf /mnt/ota/data/{id}log.tar /mnt/ota/data/log"
        cmd2 = f"adb -s {btbox} pull /mnt/ota/data/{id}log.tar {LOG_PATH}/otalog"
    else:
        cmd1 = f"adb -s {btbox} shell tar -cvf /mnt/ota/data/{id}log.tar /mnt/ota/data/log"
        cmd2 = f"adb -s {btbox} pull /mnt/ota/data/{id}log.tar {LOG_PATH}/otalog"
    runcmd(cmd1)
    runcmd(cmd2)

def pullcanlog(id):
    cmd1 = rf"rename {TEMP_PATH}\CANlog\OTAlog.blf {id}_canlog.blf"
    cmd2 = rf"move {TEMP_PATH}\CANlog\{id}_canlog.blf {LOG_PATH}\canlog"
    runcmd(cmd1)
    runcmd(cmd2)

if __name__ == '__main__':
    pullotalog("18543", "H97-B")
    # pullcanlog("123")