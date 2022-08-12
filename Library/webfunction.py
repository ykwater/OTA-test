from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from Tools.times import sleep
from Tools.value import var
from Tools.value import source
from Tools.logger import log
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
from selenium.webdriver.common.keys import Keys


class CreateCampaign(object):

    def login(self):
        """登录摩登网址"""
        self.browser = webdriver.Chrome()
        log.info('打开谷歌浏览器')
        self.browser.implicitly_wait(60)
        self.timeout = 200
        self.wait = WebDriverWait(self.browser, self.timeout)
        try:
        # 打开摩登OTA云端网址
            self.browser.get(var.V_URL)
            # 最大化网站窗口
            # sleep(2)
            self.browser.maximize_window()
            self.browser.find_element_by_xpath(source.E_SENIOR[1]).click()
            self.browser.find_element_by_xpath(source.E_GOTO[1]).click()
            # 输入用户名
            self.browser.find_element_by_name(source.E_USER[1]).send_keys(var.V_USERNAME)
            # 输入密码
            self.browser.find_element_by_name(source.E_PASS[1]).send_keys(var.V_PASSWORD)
            # 点击登录按钮
            self.browser.find_element_by_id(source.E_LOGIN[1]).click()
            log.info(f"登录{var.V_URL}成功")
            return True
        except TimeoutException:
            log.info(f"登录{var.V_URL}失败")
            return False

    def check_URL(self):
        """获取任务ID"""
        sleep(0.5)
        self.URL = self.browser.current_url
        self.URL = self.URL.split('/')[-2].split('/')[-1]
        return self.URL

    def campaign_status(self, id):
        """获取任务升级状态"""
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        apiurl = var.V_STATUSAPIURL + id
        loginurl = var.V_LOGINURL
        s = requests.session()
        s.post(loginurl, verify=False)
        response = s.get(url=apiurl, verify=False)
        result = response.json().get("updateSummaries")[0].get("name")
        if result == "SUCCESS":
            log.info('云端任务显示升级成功: SUCCESS')
            return True
        elif result == "FAILED":
            log.error('云端任务显示升级失败: FAILED')
            return False
        else:
            return None

    def getruncampaignstatus(self, id):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        apiurl = var.V_STATUSAPIURL + id
        loginurl = var.V_LOGINURL
        s = requests.session()
        s.post(loginurl, verify=False)
        response = s.get(url=apiurl, verify=False)
        campaignid = response.json().get("updateSummaries")[0].get("name")
        if campaignid == "SUCCESS":
            return False
        elif campaignid == "UNSCHEDULED":
            pass
        else:
            return True


    def click_button(self, element_value, element_item):
        """点击按钮"""
        sleep(0.5)
        try:
            self.browser.find_element_by_xpath(element_value).click()
            log.info(f"点击{element_item}成功")
            return True
        except TimeoutException:
            log.info(f"点击{element_item}失败")
            return False

    def down_box(self, element_value, element_item, name):
        """选择下拉弹框"""
        sleep(0.5)
        try:
            self.db = Select(self.browser.find_element_by_xpath(element_value))
            self.db.select_by_visible_text(name)
            log.info(f"在{element_item}选择下拉弹框{name}成功")
            return True
        except TimeoutException:
            log.info(f"在{element_item}选择下拉弹框{name}失败")
            return False

    def input_text(self, element_value, element_item, inputstr):
        """文本框输入"""
        sleep(0.5)
        try:
            # 利用xpath输入文本框
            element = self.browser.find_element_by_xpath(element_value)
            element.clear()
            element.send_keys(inputstr)
            log.info(f"在{element_item}输入文本{inputstr}成功")
            return True
        except TimeoutException:
            log.info(f"在{element_item}输入文本{inputstr}失败")
            return False

    # def input_time(self, elemtnt, mft):
    # """输入时间戳"""
    #     timestr = strftime(mft)
    #     sleep(2)
    #     # 只读文本框变为可输入文本框
    #     js = "document.getElementById(element).removeAttribute('readonly')"
    #     sleep(2)
    #     # 执行js命令
    #     self.browser.execute_script(js)
    #     # 清除文本框内容
    #     self.browser.find_element_by_id(elemtnt).clear()
    #     sleep(2)
    #     # 输入内容
    #     self.browser.find_element_by_id(elemtnt).send_keys(timestr)

    def close_web(self):
        """关闭网页"""
        sleep(1)
        return self.browser.quit(), log.info('关闭浏览器')


new = CreateCampaign()

if __name__ == '__main__':
    taskname = 'AutomationAutoTest'
    try:
        new.login()
    except OSError as err:
        print("OS error: {0}".format(err))
    new.click_button(source.E_OTAMANAGE[1], source.E_OTAMANAGE[0])
    new.click_button(source.E_CAMPAIGN[1], source.E_CAMPAIGN[0])
    new.click_button(source.E_NEWCAM[1], source.E_NEWCAM[0])
    new.input_text(source.E_CAMNAME[1], source.E_CAMNAME[0], (taskname))
    new.input_text(source.E_DESC[1], source.E_DESC[0], "KY")
    new.click_button(source.E_CREATE[1], source.E_CREATE[0])
    sleep(0.5)
    camapanid = new.check_URL()
    log.info(camapanid)
    new.down_box(source.E_MANUFA[1], source.E_MANUFA[0], var.V_MENU)
    new.down_box(source.E_BRAND[1], source.E_BRAND[0], var.V_BRAND)
    new.down_box(source.E_SERIES[1], source.E_SERIES[0], var.V_MODEL)
    new.click_button(source.E_MODELCAR[1], source.E_MODELCAR[0])
    new.click_button(source.E_SETPONE[1], source.E_SETPONE[0])
    new.input_text(source.E_INVERSION[1], source.E_INVERSION[0], "ACU")  # var.V_IHU2)
    new.click_button(source.E_SEAVERSION[1], source.E_SEAVERSION[0])
    new.click_button(source.E_SELVERSION[1], source.E_SELVERSION[0])
    new.click_button(source.E_NEXTSETP[1],source.E_NEXTSETP[0])
    new.input_text(source.E_INVIN[1], source.E_INVIN[0], var.V_VIN)
    new.click_button(source.E_SEAVIN[1], source.E_SEAVIN[0])
    new.click_button(source.E_SELVIN[1], source.E_SELVIN[0])
    new.click_button(source.E_SETPTWO[1], source.E_SETPTWO[0])
    new.input_text(source.E_EstimatedTime[1], source.E_EstimatedTime[0], '1800')
    new.down_box(source.E_POLICY[1], source.E_POLICY[0], var.V_POLICYNAME)
    new.input_text(source.E_UPNINFO[1], source.E_UPNINFO[0], 'KY')
    new.click_button(source.E_SETPTHERR[1], source.E_SETPTHERR[0])
    new.click_button(source.E_SUBMITEFOR[1], source.E_SUBMITEFOR[0])
    sleep(0.5)
    new.click_button(source.E_APPROVAL[1], source.E_APPROVAL[0])
    new.input_text(source.E_CAMPAIGNNAMEFRAME[1], source.E_CAMPAIGNNAMEFRAME[0], taskname)
    new.click_button(source.E_CAMPAIGSEARCH[1], source.E_CAMPAIGSEARCH[0])
    new.click_button(source.E_CAMPAIGSELECT[1], source.E_CAMPAIGSELECT[0])
    new.down_box(source.E_SELECTAPPROVAL[1], source.E_SELECTAPPROVAL[0], '拒绝')
    new.input_text(source.E_APPROVALNOTE[1], source.E_APPROVALNOTE[0], 'pass')
    new.click_button(source.E_SAVEBUTTON[1], source.E_SAVEBUTTON[0])
    new.close_web()
    # print(new.getruncampaignstatus("16775"))

