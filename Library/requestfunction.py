import json
import re
from urllib import parse
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from Tools.logger import log
from Tools.value import var


# 查询任务状态
def getcamp(campaignid):
    req = requests.session()
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    # 验证
    sessionToken = __authn(req,var.V_USERNAME,var.V_PASSWORD)
    # 授权
    sid = __authorize(req,var.V_USERNAME,var.V_CLIENTID,var.V_NONCE,var.V_STATE,sessionToken)
    # 获取sessionId
    sessionId = __me(req,sid)
    # 获取xl4.sso.okta.okta.sid.v2
    oktas = __session(req,var.V_CLIENTID,sessionId)

    crsfid = __csrfid(req,oktas[0],oktas[1])
    campaistutas = __campaign(req,crsfid, campaignid)
    if campaistutas:
        return True
    else:
        return False

def Request_checkcampaignstatus(campaignid):
    req = requests.session()
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    # 验证
    sessionToken = __authn(req, var.V_USERNAME, var.V_PASSWORD)
    # 授权
    sid = __authorize(req, var.V_USERNAME, var.V_CLIENTID, var.V_NONCE, var.V_STATE, sessionToken)
    # 获取sessionId
    sessionId = __me(req, sid)
    # 获取xl4.sso.okta.okta.sid.v2
    oktas = __session(req, var.V_CLIENTID, sessionId)

    crsfid = __csrfid(req, oktas[0], oktas[1])
    campaistutas = __result(req, crsfid, campaignid)
    if campaistutas:
        return True
    else:
        return False



def __authn(req,username,password):
    reqdata = {"paramlist": {"username": username, "password": password}}
    paramlist = reqdata["paramlist"]
    url = "https://excelfore.okta.com"+"/api/v1/authn"
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {"password": paramlist["password"], "username": paramlist["username"],"options": {"warnBeforePasswordExpired": True, "multiOptionalFactorEnroll": False}}
    resp = req.post(url,headers=headers,data=json.dumps(payload))
    sessionToken = json.loads(resp.text)["sessionToken"]
    return sessionToken


def __authorize(req,username,client_id,nonce,state,sessionToken):
    redirect_uri = parse.quote("http://znwl-otatest.faw.cn:9081"+"/sotauiv4")
    reqdata = {"paramlist": {"client_id": client_id, "nonce": nonce,"state":state,"redirect_uri":redirect_uri,"sessionToken":sessionToken,"username":username}}
    # resp = LoginReq.authorize(req,reqdata)
    paramlist = reqdata["paramlist"]
    url = "https://excelfore.okta.com"+"/oauth2/v1/authorize?client_id="+paramlist["client_id"]+"&nonce="+paramlist["nonce"]+"&prompt=none&redirect_uri="+paramlist["redirect_uri"]+"&response_mode=okta_post_message&response_type=id_token&sessionToken="+paramlist["sessionToken"]+"&state="+paramlist["state"]+"&scope=openid%20email"
    headers = {
        'Content-Type': 'application/json',
        'cookie': 'ln=%s' % paramlist["username"]
    }
    resp = req.get(url, headers=headers)
    # assert "data.error" not in resp.text , resp.text
    sidlist = re.findall("sid=(.+?);", str(resp.headers))
    return sidlist[0]


def __me(req,sid):
    reqdata = {"paramlist": {"sid": sid}}
    # resp = LoginReq.me(req,reqdata)
    paramlist = reqdata["paramlist"]
    url = "https://excelfore.okta.com"+"/api/v1/sessions/me"
    headers = {
        'Content-Type': 'application/json',
        'x-okta-user-agent-extended': 'okta-signin-widget-3.6.0',
        'Cookie': 'sid=%s' % paramlist["sid"]
    }
    resp = req.get(url,headers=headers)
    sessionId = json.loads(resp.text)["id"]
    return sessionId


def __session(req,client_id,sessionId):
    reqdata = {"paramlist": {"sessionId":sessionId,"client_id":client_id}}
    paramlist = reqdata["paramlist"]
    url = "https://109.244.48.12:9080/snap/omaui/sso/okta/v1/session"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    formdata = {
        "sessionId": paramlist["sessionId"],
        "baseUrl": "https://excelfore.okta.com",
        "clientId": paramlist["client_id"]
    }
    resp = req.post(url, headers=headers, data=formdata, verify=False)
    oktasidv2 = re.findall("xl4.sso.okta.okta.sid.v2=(.+?);", str(resp.headers))
    return oktasidv2[0], paramlist


def __csrfid(req,oktasidv,paramlist):
    url = "https://109.244.48.12:9080/snap/omaui/sapi/v1/csrf?path=/"
    hearders = {
        'Content-Type': 'application/json',
        'xl4.sso.okta.okta.sid.v2': oktasidv
    }
    formdata = {
        "sessionId": paramlist["sessionId"],
        "baseUrl": "https://excelfore.okta.com",
        "clientId": paramlist["client_id"]
    }
    resp1 = req.post(url, headers=hearders, data=formdata, verify=False)
    csrfid = re.findall("x-esync-csrf=(.+?);", str(resp1.headers))
    return csrfid[0]


def __campaign(req, csrfid, campaid):
    apiurl = "https://109.244.48.12:9080/snap/omaui/custom/gac/get/user/campaigns?page=0&pageSize=10&sort=null&ascending=false&withoutDrafts=false&withoutEmpty=false"
    hearders = {
        "x-esync-csrf": csrfid,
    }
    resp2 = req.post(apiurl, headers=hearders, verify=False)
    b = resp2.json().get("objects")
    for i in b:
        campaignid = i.get("id")
        if campaignid == int(campaid):
            if i.get("state") == "Running":
                log.info(f"{campaid}云端任务状态为：Running")
                return True
            else:
                log.error(f"{campaid}任务部署失败")
                return False
        else:
            pass
    log.error(f"没有查询到ID为{campaid}的任务号")
    return False


def __result(req, csrfid, campaid):
    apiurl = f"https://109.244.48.12:9080/snap/omaui/custom/gac/campaigns/updateSummaries?campaignId={campaid}"
    hearders = {
        "x-esync-csrf": csrfid,
    }
    resp2 = req.post(apiurl, headers=hearders, verify=False)
    b = resp2.json().get("updateSummaries")[0].get("name")
    if b == "SUCCESS":
        log.info('云端任务显示升级成功: SUCCESS')
        return True
    elif b == "FAILED":
        log.error('云端任务显示升级失败: FAILED')
        return False
    else:
        return None

if __name__ == '__main__':
    # getcamp("7786")
    print(Request_checkcampaignstatus("8710"))