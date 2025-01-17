import time
from lxml import etree

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class ScraperPassport:

    def __init__(self, username: str, password: str, action_type: list):
        self.username = username
        self.password = password
        self.url = "https://sso.tisi.go.th/login"
        self.action_type = action_type
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_argument('--proxy-server=http://{}:{}'.format("127.0.0.1", 1080))
        self.chrome_options.add_experimental_option("useAutomationExtension", 'False')
        self.chrome_options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"')

        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                      Object.defineProperty(navigator, 'webdriver', {
                        get: () => false
                      })
                    """
        })
        self.driver.maximize_window()

        self.result = {}

    def login(self):
        try:
            self.driver.get(self.url)
            self.driver.find_element("id", "username").send_keys(self.username)
            self.driver.find_element("id", "password").send_keys(self.password)
            self.driver.find_element(by=By.XPATH, value="//button[@type='submit']").click()
            locator = (By.XPATH, "//*[@id='wrapper']//div[@class='row colorbox-group-widget']/div[1]")
            WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(locator))
            # 等待仪表盘详情页加载完成
            self.check_parse_model()
        except Exception as e:
            raise Exception(f"Exception: Timeout waiting"
                            f" for page to load,用户账号或密码错误: {self.username},异常信息:{e}")

    def check_parse_model(self):
        try:
            if 'NSW' in self.action_type:
                self.driver.find_element(by=By.XPATH,
                                         value="//*[@id='wrapper']//div[@class='row colorbox-group-widget']/div[2]/a").click()
                NSW_locator = (By.XPATH, "//body/div[@class='container-fluid']/div[@class='col-md-6']")
                WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(NSW_locator))
                NSW_data = self.parse_NSW()
                self.result['NSW'] = NSW_data

            self.driver.find_element(by=By.XPATH,
                                     value="//*[@id='wrapper']//div[@class='row colorbox-group-widget']/div[1]/a").click()
            license_locator = (By.XPATH, "//*[@id='top']/div//ul[@class='nav menu nav-pills']/li[7]")
            WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(license_locator))
            for action in self.action_type:
                if action == "Mor5":
                    mor_data = self.parse_mor5()
                    self.result['Mor5'] = mor_data
                if action == 'Mor9':
                    mor9_data = self.parse_mor9()
                    self.result["Mor9"] = mor9_data
                if action == 'AFT':
                    AFT_data = self.parse_AFT()
                    self.result["AFT"] = AFT_data
                if action == 'AFFA':
                    AFFT_data = self.parse_AFFA()
                    self.result["AFFA"] = AFFT_data
            after_model = self.driver.find_element(by=By.XPATH,value="//*[@id='top']/div/nav/div[2]/ul[@class='nav menu nav-pills']/li[8]/a")
            ActionChains(self.driver).move_to_element(after_model).click(after_model).perform()
            self.logout()
        except Exception as e:
            raise Exception(f"该账号:{self.username}监控出现异常,请检查账号是否有误,异常信息:{e}")

    """
     解析模板Mor5
    """

    def parse_mor5(self):
        data = []
        try:
            model_locator = self.driver.find_element(by=By.XPATH,
                                                     value="//*[@id='top']/div//ul[@class='nav menu nav-pills']/li[7]")
            ActionChains(self.driver).move_to_element(model_locator).perform()
            time.sleep(1)
            self.driver.find_element(by=By.XPATH,
                                     value="//*[@id='top']/div//ul[@class='nav menu nav-pills']/li[7]/ul/li[3]").click()
            # 等待表格加载完成
            table_locator = (By.XPATH, '//*[@id="moao5List"]')
            WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(table_locator))
            page_result = self.driver.page_source
            tree = etree.HTML(page_result, etree.HTMLParser())
            tr_list = tree.xpath("//*[@id='moao5List']/tbody/tr")
            for tr in tr_list:
                item = {}
                if tr.xpath("./td[2]/text()"):
                    item["id"] = tr.xpath("./td[2]/text()")[0].strip()
                if tr.xpath("./td[3]/text()"):
                    item["applicant"] = tr.xpath("./td[3]/text()")[0].strip()
                if tr.xpath("./td[4]/text()"):
                    item["taxNumber"] = tr.xpath("./td[4]/text()")[0].strip()
                if tr.xpath("./td[5]/text()"):
                    item["mokId"] = tr.xpath("./td[5]/text()")[0].strip()
                if tr.xpath("./td[6]/text()"):
                    item["standardName"] = tr.xpath("./td[6]/text()")[0].strip()
                if tr.xpath("./td[7]//text()"):
                    item["applicationDate"] = "".join(tr.xpath("./td[7]//text()")).strip()
                else:
                    item["applicationDate"] = ""
                if tr.xpath("./td[8]//span[@class='show_status']"):
                    str_list = "".join(tr.xpath("./td[8]//span[@class='show_status']//text()"))
                    item["status"] = str_list.strip()
                else:
                    item["status"] = ""
                if tr.xpath("./td[9]//text()"):
                    str_list = "".join(tr.xpath("./td[9]//text()"))
                    item["companyName"] = str_list.strip().replace("\r", "").replace("\n", "").replace("    ", "")
                data.append(item)
        except Exception as e:
            raise f"MOR 5 模块监控失败!请重新启动，并检查网站是否有更新!:{e}"
        return data

    """
    解析mor9
    """

    def parse_mor9(self):
        data = []
        try:
            model_locator = self.driver.find_element(by=By.XPATH,
                                                     value="//*[@id='top']/div//ul[@class='nav menu nav-pills']/li[7]")
            ActionChains(self.driver).move_to_element(model_locator).perform()
            time.sleep(1)
            self.driver.find_element(by=By.XPATH,
                                     value="//*[@id='top']/div//ul[@class='nav menu nav-pills']/li[7]/ul/li[8]").click()

            # 等待表格加载完成
            table_locator = (By.XPATH, '//*[@id="moao9List"]')
            WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(table_locator))
            page_result = self.driver.page_source
            tree = etree.HTML(page_result, etree.HTMLParser())
            tr_list = tree.xpath("//*[@id='moao9List']/tbody/tr")
            for tr in tr_list:
                item = {}
                if tr.xpath("./td[2]//text()"):
                    item["MOR9_APPLY_CODE"] = tr.xpath("./td[2]//text()")[0].strip()
                if tr.xpath("./td[3]//text()"):
                    item["MOR9_APPLY_NAME"] = tr.xpath("./td[3]/text()")[0].strip()
                if tr.xpath("./td[4]//text()"):
                    item["MOR9_TAX"] = tr.xpath("./td[4]//text()")[0].strip()
                if tr.xpath("./td[5]//text()"):
                    item["MOR9_TIS_CODE"] = tr.xpath("./td[5]//text()")[0].strip()
                if tr.xpath("./td[6]//text()"):
                    item["MOR9_STANDARD_NAME"] = tr.xpath("./td[6]//text()")[0].strip()
                if tr.xpath("./td[7]//text()"):
                    item["MOR9_LICENSE_CODE"] = tr.xpath("./td[7]//text()")[0].strip()
                if tr.xpath("./td[8]//text()"):
                    item["MOR9_APPLY_DATE"] = tr.xpath("./td[8]//text()")[0].strip()
                else:
                    item["MOR9_APPLY_DATE"] = None
                if tr.xpath("./td[9]/p/span/text()"):
                    item["MOR9_STATUS"] = tr.xpath("./td[9]/p/span/text()")[0].strip()
                else:
                    item["MOR9_STATUS"] = ""
                if tr.xpath("./td[10]//text()"):
                    item["MOR9_OPERATE_NAME"] = "".join(tr.xpath("./td[10]//text()")).strip().replace(": ", "")
                data.append(item)
        except Exception as e:
            raise f"MOR 9 模块监控失败!请重新启动，并检查网站是否有更新!:{e}"
        return data

    def parse_AFFA(self):
        data = []
        try:
            model_locator = self.driver.find_element(by=By.XPATH,
                                                     value="//*[@id='top']/div//ul[@class='nav menu nav-pills']/li[6]")
            ActionChains(self.driver).move_to_element(model_locator).perform()
            time.sleep(1)
            self.driver.find_element(by=By.XPATH,
                                     value="//*[@id='top']/div//ul[@class='nav menu nav-pills']/li[6]/ul/li[2]").click()
            table_locator = (By.XPATH, '//*[@id="factoryList"]')
            WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(table_locator))
            page_result = self.driver.page_source
            tree = etree.HTML(page_result, etree.HTMLParser())
            tr_list = tree.xpath("//*[@id='factoryList']/tbody/tr")
            for tr in tr_list:
                item = {}
                if tr.xpath("./td[2]//text()"):
                    item["AFFA_appId"] = tr.xpath("./td[2]//text()")[0].strip()
                else:
                    item["AFFA_appId"] = ""
                if tr.xpath("./td[3]//text()"):
                    item["AFFA_TIS_CODE"] = tr.xpath("./td[3]//text()")[0].strip()
                else:
                    item["AFFA_TIS_CODE"] = ""
                if tr.xpath("./td[4]//text()"):
                    item["AFFA_APP_NAME"] = tr.xpath("./td[4]//text()")[0].strip()
                else:
                    item["AFFA_APP_NAME"] = ""
                if tr.xpath("./td[5]//text()"):
                    item["AFFA_APP_LICENSE"] = tr.xpath("./td[5]//text()")[0].strip()
                else:
                    item["AFFA_APP_LICENSE"] = ""
                if tr.xpath("./td[6]/text()"):
                    item["applicationDate"] = "".join(tr.xpath("./td[6]//text()")).strip()
                else:
                    item["applicationDate"] = ""
                if tr.xpath("./td[7]/text()"):
                    str_list = "".join(tr.xpath("./td[7]//text()"))
                    item["status"] = str_list.strip()
                else:
                    item["status"] = ""
                data.append(item)
        except Exception as e:
            raise f"AFFA 模块监控失败!请重新启动，并检查网站是否有更新!:{e}"
        return data

    def parse_AFT(self):
        data = []
        try:
            model_locator = self.driver.find_element(by=By.XPATH,
                                                     value="//*[@id='top']/div//ul[@class='nav menu nav-pills']/li[6]")
            ActionChains(self.driver).move_to_element(model_locator).perform()
            time.sleep(1)
            self.driver.find_element(by=By.XPATH,
                                     value="//*[@id='top']/div//ul[@class='nav menu nav-pills']/li[6]/ul/li[3]").click()
            table_locator = (By.XPATH, '//*[@id="productList"]')
            WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(table_locator))
            page_result = self.driver.page_source
            tree = etree.HTML(page_result, etree.HTMLParser())
            tr_list = tree.xpath("//*[@id='productList']/tbody/tr")
            for tr in tr_list:
                item = {}
                if tr.xpath("./td[2]/text()"):
                    item["ATF_appId"] = tr.xpath("./td[2]/text()")[0].strip()
                if tr.xpath("./td[3]//text()"):
                    item["ATF_TIS_CODE"] = "".join(tr.xpath("./td[3]//text()")).strip()
                if tr.xpath("./td[4]/text()"):
                    item["ATF_APP_NAME"] = tr.xpath("./td[4]/text()")[0].strip()
                if tr.xpath("./td[5]/text()"):
                    item["AFT_APP_LICENSE"] = tr.xpath("./td[5]/text()")[0].strip()
                if tr.xpath("./td[6]/text()"):
                    item["applicationDate"] = tr.xpath("./td[6]/text()")[0].strip()
                else:
                    item["applicationDate"] = ""
                if tr.xpath("./td[7]/text()"):
                    item["status"] = "".join(tr.xpath("./td[7]/text()")).strip()
                else:
                    item["status"] = ""
                data.append(item)
        except Exception as e:
            raise f"AFT 模块监控失败!请重新启动，并检查网站是否有更新!:{e}"
        return data

    def parse_NSW(self):
        data = []
        try:
            self.driver.find_element(by=By.XPATH,
                                     value="//body/div[@class='container-fluid']/div[@class='col-md-6']/div/a").click()
            table_locator = (By.XPATH, '//*[@id="table6"]')
            WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(table_locator))
            page_source = self.driver.page_source
            tree = etree.HTML(page_source, etree.HTMLParser())
            tr_list = tree.xpath("//*[@id='table6']/tbody/tr")
            for tr in tr_list:
                item = {}
                if tr.xpath("./td[1]/font/text()"):
                    item["NSW_CODE"] = tr.xpath("./td[1]/font/text()")[0].strip()
                if tr.xpath("./td[2]/font/text()"):
                    item["NSW_INVOICE"] = tr.xpath("./td[2]/font/text()")[0].strip()
                if tr.xpath("./td[3]/font/text()"):
                    item["NSW_INVOICE_DATE"] = tr.xpath("./td[3]/font/text()")[0].strip()
                if tr.xpath("./td[4]/font/text()"):
                    item["NSW_PRO_NUMBER"] = tr.xpath("./td[4]/font/text()")[0].strip()
                if tr.xpath("./td[5]/font/text()"):
                    item["NSW_RPG"] = tr.xpath("./td[5]/font/text()")[0].strip()
                if tr.xpath("./td[6]/font/text()"):
                    item["NSW_APPLY_DATE"] = tr.xpath("./td[6]/font/text()")[0].strip()
                else:
                    item["NSW_INVOICE_DATE"] = ""
                if tr.xpath("./td[8]/font/text()"):
                    item["NSW_APPLY_PASS_DATE"] = tr.xpath("./td[8]/font/text()")[0].strip()
                else:
                    item["NSW_APPLY_PASS_DATE"] = ""
                if tr.xpath("./td[9]/font/text()"):
                    item["NSW_APPLY_STATUS"] = tr.xpath("./td[9]/font/text()")[0].strip()
                else:
                    item["NSW_APPLY_STATUS"] = ""
                data.append(item)
            self.driver.find_element(by=By.XPATH,
                                     value="//body/div[@class='container-fluid']/ol/li[@class='active']/font/a").click()
            locator = (By.XPATH,
                       "//*[@id='wrapper']/nav/div[@class='navbar-header']/ul[@class='nav navbar-top-links navbar-right pull-right']/li[2]/a")
            WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(locator))
        except Exception as e:
            raise f"NSW 模块监控失败!请重新启动，并检查网站是否有更新!:{e}"
        return data

    """
    退出登录
    """

    def logout(self):
        try:
            self.driver.find_element(by=By.XPATH,value="//*[@id='wrapper']/nav/div[@class='navbar-header']/ul[@class='nav navbar-top-links navbar-right pull-right']/li[2]/a/i").click()
            time.sleep(2)
            self.driver.find_element(By.XPATH, value='//*[@id="wrapper"]/div[2]/div/div[1]/div[2]/a').click()
        except Exception as e:
            raise f"退出登录失败!:{e}"

    def close(self):
        self.driver.quit()
        print(f"关闭浏览器,账号:{self.username}采集完成,采集模块:{self.action_type}")
        return self.result


if __name__ == '__main__':
    # scraper = ScraperPassport("0115566026132", "daican866@qq", ['AFFA', 'Mor5', "AFT"])
    scraper = ScraperPassport("0105548160264", "K@ming0101", ["Mor9"])
    scraper.login()
    # scraper.logout()
    scraper.close()
