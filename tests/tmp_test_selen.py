import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_BankAdminLogin(self):
        driver = self.driver
        driver.get('localhost:8080')
        elem = driver.find_element_by_name('username')
        elem.send_keys('1234567890')
        elem = driver.find_element_by_name('password')
        elem.send_keys('123456')
        elem.send_keys(Keys.ENTER)
        elem = driver.find_elements_by_id('navbar')
        self.assertNotEqual(len(elem), 0)

    def test_BankAdminAnnualProfit(self):
        driver = self.driver
        driver.get('localhost:8080')
        elem = driver.find_element_by_name('username')
        elem.send_keys('1234567890')
        elem = driver.find_element_by_name('password')
        elem.send_keys('123456')
        elem.send_keys(Keys.ENTER)
        elem = driver.find_element_by_xpath("//a[@href='/bank/define_annual_profit']")
        elem.click()
        elem = driver.find_element_by_name("annual_profit")
        elem.send_keys('20')
        elem.send_keys(Keys.ENTER)
        elem = driver.find_elements_by_xpath("//div[@role='alert']")
        self.assertNotEqual(len(elem), 0)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()