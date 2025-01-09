import time
from lxml import etree

from selenium import webdriver
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
        # self.chrome_options.add_argument("--headless")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_argument('--proxy-server=http://{}:{}'.format("127.0.0.1", 7890))
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

    def login(self):
        self.driver.get(self.url)
        self.driver.find_element("id", "username").send_keys(self.username)
        self.driver.find_element("id", "password").send_keys(self.password)
        time.sleep(2)
        self.driver.find_element(by=By.XPATH, value="//button[@type='submit']").click()
        locator = (By.XPATH, "//*[@id='wrapper']//div[@class='row colorbox-group-widget']/div[1]")
        WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(locator))
        # 等待仪表盘详情页加载完成
        self.check_parse_model()

    def check_parse_model(self):
        if 'NSW' in self.action_type:
            self.driver.find_element(by=By.XPATH,
                                     value="//*[@id='wrapper']//div[@class='row colorbox-group-widget']/div[2]/a").click()
            NSW_locator = (By.XPATH, "//body/div[@class='container-fluid']/div[@class='col-md-6']")
            WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(NSW_locator))
            self.parse_NSW()

        self.driver.find_element(by=By.XPATH,
                                 value="//*[@id='wrapper']//div[@class='row colorbox-group-widget']/div[1]/a").click()
        license_locator = (By.XPATH, "//*[@id='top']/div//ul[@class='nav menu nav-pills']/li[7]")
        WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(license_locator))
        for action in self.action_type:
            if action == "Mor5":
                mor_data = self.parse_mor5()
                print(mor_data)
            if action == 'Mor9':
                self.parse_mor9()
            if action == 'AFT':
                AFT_data = self.parse_AFT()
                print(AFT_data)
            if action == 'AFFA':
                AFFT_data = self.parse_AFFA()
                print(AFFT_data)
        after_model = self.driver.find_element(by=By.XPATH,
                                               value="//*[@id='top']/div/nav/div[2]/ul[@class='nav menu nav-pills']/li[8]/a")
        ActionChains(self.driver).move_to_element(after_model).click(after_model).perform()

    """
     解析模板Mor5
    """

    def parse_mor5(self):
        data = []
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
            if tr.xpath("./td[7]/text()"):
                item["applicationDate"] = tr.xpath("./td[7]/text()")[0].strip()
            if tr.xpath("./td[8]//span[@class='show_status']"):
                str_list = "".join(tr.xpath("./td[8]//span[@class='show_status']//text()"))
                item["status"] = str_list.strip()
            if tr.xpath("./td[9]"):
                str_list = "".join(tr.xpath("./td[9]/text()"))
                item["companyName"] = str_list.strip().replace("\r", "").replace("\n", "").replace("    ", "")
            data.append(item)
        return data

    """
    解析mor9
    """

    def parse_mor9(self):
        model_locator = self.driver.find_element(by=By.XPATH,
                                                 value="//*[@id='top']/div//ul[@class='nav menu nav-pills']/li[7]")
        ActionChains(self.driver).move_to_element(model_locator).perform()
        time.sleep(1)
        self.driver.find_element(by=By.XPATH,
                                 value="//*[@id='top']/div//ul[@class='nav menu nav-pills']/li[7]/ul/li[1]").click()

        # 等待表格加载完成
        table_locator = (By.XPATH, '//*[@id="moao1List"]')
        WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(table_locator))
        page_result = self.driver.page_source

    def parse_AFFA(self):
        data = []
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
            if tr.xpath("./td[3]//text()"):
                item["AFFA_TIS_CODE"] = tr.xpath("./td[3]//text()")[0].strip()
            if tr.xpath("./td[4]//text()"):
                item["AFFA_APP_NAME"] = tr.xpath("./td[4]//text()")[0].strip()
            if tr.xpath("./td[5]//text()"):
                item["AFFA_APP_LICENSE"] = tr.xpath("./td[5]//text()")[0].strip()
            if tr.xpath("./td[6]/font/font/text()"):
                item["applicationDate"] = tr.xpath("./td[6]/font/font/text()")[0].strip()
            if tr.xpath("./td[7]/font/font/text()"):
                str_list = "".join(tr.xpath("./td[7]/font//text()"))
                item["status"] = str_list.strip()
            data.append(item)
        return data

    def parse_AFT(self):
        data = []
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
            if tr.xpath("./td[3]/text()"):
                item["ATF_TIS_CODE"] = tr.xpath("./td[3]/text()")[0].strip()
            if tr.xpath("./td[4]/text()"):
                item["ATF_APP_NAME"] = tr.xpath("./td[4]/text()")[0].strip()
            if tr.xpath("./td[5]/text()"):
                item["AFFA_APP_LICENSE"] = tr.xpath("./td[5]/text()")[0].strip()
            if tr.xpath("./td[6]/text()"):
                item["applicationDate"] = tr.xpath("./td[6]/text()")[0].strip()
            if tr.xpath("./td[7]/font/font/text()"):
                item["sataus"] = tr.xpath("./td[7]/text()").strip()
            data.append(item)
        return data

    def parse_NSW(self):
        self.driver.find_element(by=By.XPATH,
                                 value="//body/div[@class='container-fluid']/div[@class='col-md-6']/div/a").click()
        time.sleep(3)
        self.driver.find_element(by=By.XPATH,
                                 value="//body/div[@class='container-fluid']/ol/li[@class='active']/font/a").click()
        locator = (By.XPATH,
                   "//*[@id='wrapper']/nav/div[@class='navbar-header']/ul[@class='nav navbar-top-links navbar-right pull-right']/li[2]/a")
        WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(locator))
        time.sleep(2)

    """
    退出登录
    """

    def logout(self):
        self.driver.find_element(by=By.XPATH,
                                 value="//*[@id='wrapper']/nav/div[@class='navbar-header']/ul[@class='nav navbar-top-links navbar-right pull-right']/li[2]/a/i").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, value='//*[@id="wrapper"]/div[2]/div/div[1]/div[2]/a').click()

    def close(self):
        self.driver.quit()


if __name__ == '__main__':
    # scraper = ScraperPassport("0115566026132", "daican866@qq", ['AFFA', 'Mor5', "AFT"])
    scraper = ScraperPassport("0115566026132", "daican866@qq", ['NSW'])
    scraper.login()
    scraper.logout()
    scraper.close()
