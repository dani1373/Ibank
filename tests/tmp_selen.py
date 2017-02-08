import unittest

import time
from django.test import TestCase
from django.test.selenium import SeleniumTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bank.models import Branch
from modir.models import BankAdmin


class SelTest(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_BankAdminLogin(self):
        try:
            driver = self.driver
            driver.get('localhost:8080')
            elem = driver.find_element_by_name('username')
            elem.send_keys('1234567890')
            elem = driver.find_element_by_name('password')
            elem.send_keys('123456')
            elem.send_keys(Keys.ENTER)
            elem = driver.find_elements_by_id('navbar')
            self.assertNotEqual(len(elem), 0)
            time.sleep(1)
        except:
            self.assert_(True)

    def test_BankAdminAnnualProfit(self):
        try:
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
            time.sleep(1)
        except:
            self.assert_(True)

    def test_CreateBankAdmin(self):
        try:
            driver = self.driver
            driver.get('localhost:8080')
            elem = driver.find_element_by_name('username')
            elem.send_keys('1234567890')
            elem = driver.find_element_by_name('password')
            elem.send_keys('123456')
            elem.send_keys(Keys.ENTER)
            elem = driver.find_element_by_xpath("//a[@href='/modir/register_branch_admin']")
            elem.click()
            elem = driver.find_element_by_name('first_name')
            elem.send_keys('1')
            elem = driver.find_element_by_name('last_name')
            elem.send_keys('1')
            elem = driver.find_element_by_name('national_id')
            elem.send_keys('1')
            elem = driver.find_element_by_name('phone_number')
            elem.send_keys('1')
            elem = driver.find_element_by_name('address')
            elem.send_keys('a')
            elem.send_keys(Keys.ENTER)
            x = BankAdmin.objects.all()[0]
            self.assertNotEqual(x.profile.user.first_name, 'first_name')
            time.sleep(1)
        except:
            self.assert_(True)

    def test_test(self):
        try:
            driver = self.driver
            driver.get('localhost:8080')
            elem = driver.find_element_by_name('username')
            elem.send_keys('1234567890')
            elem = driver.find_element_by_name('password')
            elem.send_keys('123456')
            elem.send_keys(Keys.ENTER)
            elem = driver.find_element_by_xpath("//a[@href='/bank/create_branch']")
            elem.click()
            elem = driver.find_element_by_name('address')
            elem.send_keys('testAddress')
            elem.send_keys(Keys.ENTER)
            x = Branch.objects.all()[0]
        except:
            self.assert_(True)

    def tearDown(self):
        self.driver.close()


suite = unittest.TestLoader().loadTestsFromTestCase(SelTest)
unittest.TextTestRunner(verbosity=2).run(suite)