from BaseData.readconfig import ini
from BaseData.readyaml import elment
from Tools.times import strftime


class ReadVar(object):
    # 云端地址
    V_URL = ini.get('LOGIN', 'url')
    # 用户名
    V_USERNAME = ini.get('LOGIN', 'username')
    # 用户密码
    V_PASSWORD = ini.get('LOGIN', 'password')
    # 升级策略
    V_POLICYNAME = ini.get('LOGIN', 'policyname')
    # 制造商
    V_MENU = ini.get('LOGIN', 'menu')
    # 品牌
    V_BRAND = ini.get('LOGIN', 'brand')
    # 车型
    V_MODEL = ini.get('LOGIN', 'vmodel')

    # 安卓截图保存路径
    V_SHOTPATH = ini.get("CHARTADDR", "shotpath")

    # 时间格式
    V_FMT = ini.get('CAMPAIGN', 'fmt')
    V_VIN = ini.get('CAMPAIGN', 'vin')
    V_STRTIME = "AutoTest" + strftime(V_FMT)

    # ECU版本
    V_ACU_A = ini.get("ECU", "ACU_1")
    V_ACU_B = ini.get("ECU", "ACU_2")
    V_TBOX_A = ini.get("ECU", "TBOX_1")
    V_TBOX_B = ini.get("ECU", "TBOX_2")



    # 预约升级按钮
    V_UPDATE = tuple(eval(ini.get("COORDINATE", "update")))
    # # 确定按钮
    V_CONFIRMTIME = tuple(eval(ini.get("COORDINATE", "confirmtime")))
    # 升级结果按钮
    V_UPDATECOMPLETED = tuple(eval(ini.get("COORDINATE", "updatecompleted")))
    V_RETRY = tuple(eval(ini.get("COORDINATE", "policyfail")))

    # 云端接口
    V_LOGINURL = ini.get('APIURL', 'login_url')
    V_STATUSAPIURL = ini.get('APIURL', 'statusapiurl')
    V_CLIENTID = ini.get('APIURL', 'client_id')
    V_NONCE = ini.get('APIURL', 'nonce')
    V_STATE = ini.get('APIURL', 'state')

    V_YEAR = ini.get("DATE", "YEAR")
    V_BTBOX = ini.get("DEVICESID", "B_TBOX")
    V_BIVI = ini.get("DEVICESID", "B_IVI")


class ReadSource(object):
    E_SENIOR = elment['高级']
    E_GOTO = elment['继续前往']
    E_USER = elment['用户名框']
    E_PASS = elment['用户密码框']
    E_LOGIN = elment['登录按钮']
    E_OTAMANAGE = elment['OTA管理按钮']
    E_CAMPAIGN = elment['升级任务按钮']
    E_NEWCAM = elment['新建任务按钮']
    E_CAMNAME = elment['任务名称框']
    E_DESC = elment['任务描述框']
    E_CREATE = elment['创建按钮']
    E_MANUFA = elment['制造商']
    E_BRAND = elment['品牌']
    E_SERIES = elment['车系']
    E_MODELCAR = elment['车型按钮']
    E_INVERSION = elment['版本输入框']
    E_SEAVERSION = elment['版本搜索按钮']
    E_SELVERSION = elment['选择版本号']
    E_SETPONE = elment['第一步']
    E_NEXTSETP = elment['下一步']
    E_INVIN = elment['VIN输入框']
    E_SEAVIN = elment['VIN搜索按钮']
    E_SELVIN = elment['选择VIN']
    E_SETPTWO = elment['第二步']
    E_EstimatedTime = elment['预估时间']
    E_POLICY = elment['升级策略']
    E_UPNINFO = elment['升级信息']
    E_SETPTHERR = elment['第三步']
    E_SUBMITEFOR = elment['申请批准']
    E_APPROVAL = elment['审批按钮']
    E_CAMPAIGNNAMEFRAME = elment['任务名称搜索框']
    E_CAMPAIGSEARCH = elment['任务搜索按钮']
    E_CAMPAIGSELECT = elment['任务选择按钮']
    E_SELECTAPPROVAL = elment['选择批准']
    E_APPROVALNOTE = elment['批准描述框']
    E_SAVEBUTTON = elment['保存按钮']


var = ReadVar()
source = ReadSource()
if __name__ == '__main__':
    print(type(var.V_UPDATE), var.V_UPDATE)
