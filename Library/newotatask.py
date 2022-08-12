from Library.webfunction import new
from Tools.value import var
from Tools.value import source
from Tools.logger import *
from Tools.times import *


def Web_createcampaign(value1,value2,ecupackage):
    taskname = f"{value1}_AutomationAutoTest"
    try:
        new.login()
        sleep(5)
        new.click_button(source.E_OTAMANAGE[1], source.E_OTAMANAGE[0])
        new.click_button(source.E_CAMPAIGN[1], source.E_CAMPAIGN[0])
        new.click_button(source.E_NEWCAM[1], source.E_NEWCAM[0])
        new.input_text(source.E_CAMNAME[1], source.E_CAMNAME[0], (taskname))
        new.input_text(source.E_DESC[1], source.E_DESC[0], "KY")
        new.click_button(source.E_CREATE[1], source.E_CREATE[0])
        sleep(1)
        camapanid = new.check_URL()
        log.info(camapanid)
        new.down_box(source.E_MANUFA[1], source.E_MANUFA[0], var.V_MENU)
        new.down_box(source.E_BRAND[1], source.E_BRAND[0], var.V_BRAND)
        new.down_box(source.E_SERIES[1], source.E_SERIES[0], var.V_MODEL)
        new.click_button(source.E_MODELCAR[1], source.E_MODELCAR[0])
        new.click_button(source.E_SETPONE[1], source.E_SETPONE[0])
        new.input_text(source.E_INVERSION[1], source.E_INVERSION[0], ecupackage)  # var.V_IHU2)
        new.click_button(source.E_SEAVERSION[1], source.E_SEAVERSION[0])
        sleep(1)
        new.click_button(source.E_SELVERSION[1], source.E_SELVERSION[0])
        new.click_button(source.E_NEXTSETP[1], source.E_NEXTSETP[0])
        new.input_text(source.E_INVIN[1], source.E_INVIN[0], var.V_VIN)
        new.click_button(source.E_SEAVIN[1], source.E_SEAVIN[0])
        new.click_button(source.E_SELVIN[1], source.E_SELVIN[0])
        new.click_button(source.E_SETPTWO[1], source.E_SETPTWO[0])
        new.input_text(source.E_EstimatedTime[1], source.E_EstimatedTime[0], '1800')
        new.down_box(source.E_POLICY[1], source.E_POLICY[0], var.V_POLICYNAME)
        new.input_text(source.E_UPNINFO[1], source.E_UPNINFO[0], 'KY')
        new.click_button(source.E_SETPTHERR[1], source.E_SETPTHERR[0])
        new.click_button(source.E_SUBMITEFOR[1], source.E_SUBMITEFOR[0])
        sleep(1)
        new.click_button(source.E_APPROVAL[1], source.E_APPROVAL[0])
        new.input_text(source.E_CAMPAIGNNAMEFRAME[1], source.E_CAMPAIGNNAMEFRAME[0], taskname)
        new.click_button(source.E_CAMPAIGSEARCH[1], source.E_CAMPAIGSEARCH[0])
        sleep(1)
        new.click_button(source.E_CAMPAIGSELECT[1], source.E_CAMPAIGSELECT[0])
        new.down_box(source.E_SELECTAPPROVAL[1], source.E_SELECTAPPROVAL[0], '批准')
        new.input_text(source.E_APPROVALNOTE[1], source.E_APPROVALNOTE[0], 'pass')
        new.click_button(source.E_SAVEBUTTON[1], source.E_SAVEBUTTON[0])
        new.close_web()
        sleep(1)
        now_time = timestamp()
        return now_time, camapanid
    except Exception as e:
        log.error(e)
        return False


if __name__ == '__main__':
    a = Web_createcampaign("TBOX", "不同版本","AM8_TBOX_8550003AMV09S.T5A_Diff")
    print(a)