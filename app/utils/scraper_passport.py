import time

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

    def login(self):
        self.driver.get(self.url)
        self.driver.find_element("id", "username").send_keys(self.username)
        self.driver.find_element("id", "password").send_keys(self.password)
        time.sleep(2)
        self.driver.find_element(by=By.XPATH, value="//button[@type='submit']").click()
        locator = (By.XPATH, "//*[@id='wrapper']//div[@class='row colorbox-group-widget']/div[1]")
        WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(locator))
        # 等待仪表盘详情页加载完成
        self.driver.find_element(by=By.XPATH,
                                 value="//*[@id='wrapper']//div[@class='row colorbox-group-widget']/div[1]/a").click()
        license_locator = (By.XPATH, "//*[@id='top']/div//ul[@class='nav menu nav-pills']/li[7]")
        WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(license_locator))
        for action in self.action_type:
            if action == 1:
                self.parse_model_one()
            elif action == 5:
                self.parse_model_five()

    """
     解析模板M.5
    """

    def parse_model_five(self):
        model_locator = self.driver.find_element(by=By.XPATH,
                                                 value="//*[@id='top']/div//ul[@class='nav menu nav-pills']/li[7]")
        ActionChains(self.driver).move_to_element(model_locator).perform()
        time.sleep(1)
        self.driver.find_element(by=By.XPATH,
                                 value="//*[@id='top']/div//ul[@class='nav menu nav-pills']/li[7]/ul/li[3]").click()

        # 等待表格加载完成
        table_locator = (By.XPATH, '//*[@id="moao5List"]')
        WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(table_locator))
        #
        page_result = self.driver.page_source
        time.sleep(10)
        with open("page_result.html", "w", encoding="utf-8") as fp:
            fp.write(page_result)
            fp.close()
        print("保存成功")

    def parse_model_one(self):
        model_locator = self.driver.find_element(by=By.XPATH,
                                                 value="//*[@id='top']/div//ul[@class='nav menu nav-pills']/li[7]")
        ActionChains(self.driver).move_to_element(model_locator).perform()
        time.sleep(1)
        self.driver.find_element(by=By.XPATH,
                                 value="//*[@id='top']/div//ul[@class='nav menu nav-pills']/li[7]/ul/li[1]").click()

        # 等待表格加载完成
        table_locator = (By.XPATH, '//*[@id="moao1List"]')
        WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(table_locator))
        #
        page_result = self.driver.page_source
        time.sleep(10)
        with open("page_result_1.html", "w", encoding="utf-8") as fp:
            fp.write(page_result)
            fp.close()
        print("保存成功")

    def close(self):
        self.driver.quit()


if __name__ == '__main__':
    scraper = ScraperPassport("0115566026132", "daican866@qq", [1, 5])
    scraper.login()

    scraper.close()
