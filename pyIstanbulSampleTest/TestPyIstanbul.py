# coding=utf-8
import unittest
import logging

import os

import sys

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestPyIstanbul(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.baseUrl = "http://pyistanbul.org"
        self.wait = WebDriverWait(self.driver,10)
        self.driver.get(self.baseUrl)
        self.waitForPageLoad("#oreilly-ug")

        # Datas
        self.peoplesSelector = "ul.people > li > p > strong"
        self.aboutUsLink = self.baseUrl + "/hakkimizda/"
        self.presentationsLink = self.baseUrl + "/presentations/"
        self.peopleLink = self.baseUrl + "/people/"
        self.jobsLink = self.baseUrl + "/jobs/"
        self.samplePeopleName = "Ali Göktaş"


    # Wait for load last element in html doc -- Parameter is should be css selector
    def waitForPageLoad(self,element):
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, element)))
        logging.info("Page is loaded")

    # Tour in links
    def linkHunter(self, platform):
            self.links = self.driver.find_elements_by_css_selector("a")

            for link in self.links:
                attribute = str(link.get_attribute("href"))

                # Check current url equality
                if platform in attribute:
                    link.click()
                    self.assertEqual(attribute,self.driver.current_url)
                    break


    # Check the availability of links
    def testCheckLinks(self):

        logo = self.driver.find_element_by_id("logo")
        logo.click()

        self.waitForPageLoad("#github")

        self.assertIn(self.baseUrl,self.driver.current_url)

        self.driver.get(self.baseUrl)

        self.waitForPageLoad("#github")

        self.linkHunter("twitter")

    # Check the availability of tabs
    def testCheckTabs(self):

        aboutUsTab = self.driver.find_element_by_css_selector('a[href="/hakkimizda/"]')
        aboutUsTab.click()

        self.waitForPageLoad('a[href="http://jspyconf.org"]')
        assert self.aboutUsLink == self.driver.current_url

        presentationsTab = self.driver.find_element_by_css_selector('a[href="/presentations/"]')
        presentationsTab.click()

        self.waitForPageLoad(".presentations")

        assert self.presentationsLink == self.driver.current_url

        peopleTab = self.driver.find_element_by_css_selector('a[href="/people/"]')
        peopleTab.click()

        self.waitForPageLoad(".people")

        assert self.peopleLink == self.driver.current_url

        jobsTab = self.driver.find_element_by_css_selector('a[href="/jobs/"]')
        jobsTab.click()

        self.waitForPageLoad(".jobs")

        assert self.jobsLink == self.driver.current_url

    # Access all peoples and go selected home url
    def testPeopleFailCase(self):
        try:
            self.driver.find_element_by_css_selector('a[href="/people/"]').click()
            self.waitForPageLoad(".people")

            self.assertEqual(self.peopleLink, self.driver.current_url)

            peoples = self.driver.find_elements_by_css_selector(self.peoplesSelector)

            for member in peoples:
                if member.text == self.samplePeopleName:
                    member.find_element_by_xpath("..").find_element_by_css_selector(".fa.fa-home").click()
                    break

            self.driver.find_element_by_css_selector("#logo").click()
        except Exception as e:
            exception_type, exception_message, traceback = sys.exc_info()

            filename = os.path.split(traceback.tb_frame.f_code.co_filename)[1]

            line_number = traceback.tb_lineno

            logging.error("\n Exception type : {},"
                            "\n File name : {},"
                            "\n Line Number : {}".format(type(e).__name__, filename, line_number))


    # Last works for tests
    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()