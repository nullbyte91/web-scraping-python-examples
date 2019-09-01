from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json
import pdb
from BeautifulSoup import BeautifulSoup
import pandas as pd
import time 

class ZerodhaLogin(object):
   def __init__( self ):
      self.timeout = 5
      self.loadCredentials()
      self.driver = webdriver.Chrome()
      self.small_case_discover_uri = "https://smallcase.zerodha.com/discover/all?count=51"
      self.small_case_base_uri = "https://smallcase.zerodha.com/smallcase/"
      self.timeout_count =0
      self.small_cases_id = []
   def getCssElement( self, cssSelector ):
      '''
      To make sure we wait till the element appears
      '''
      return WebDriverWait( self.driver, self.timeout ).until( EC.presence_of_element_located( ( By.CSS_SELECTOR, cssSelector ) ) )

   def loadCredentials( self ):
      with open( "credentials.json") as credsFile:
         data = json.load( credsFile )
         self.username = data[ 'username' ]
         self.password = data[ 'password' ]
         self.s_password = data[ 's_password' ] # for 2FA

   def doLogin( self ):
      # Open the Smallcase URI
      self.driver.get(self.small_case_discover_uri)
      self.driver.find_element_by_xpath('//div[@class="LoginButton__text___3T8zV"]').click()
      try:
         # Let login with Zerotha Account
         passwordField = self.getCssElement( "input[placeholder=Password]" ).send_keys( self.password )
         #passwordField.send_keys( self.password )
         userNameField = self.getCssElement( "input[placeholder='User ID']" ).send_keys( self.username )
         #userNameField.send_keys( self.username )
         loginButton = self.getCssElement( "button[type=submit]" )
         loginButton.click()
         time.sleep(10)
         s_passwordField = self.getCssElement( "input[placeholder='PIN']").send_keys( self.s_password )
         #s_passwordField.send_keys( self.s_password )
         ContinueButton = self.getCssElement( "button[type=submit]" )
         ContinueButton.click()
         content = self.driver.page_source
         soup = BeautifulSoup(content)
         print (soup)
         for a in soup.findAll(attrs={'class':'DiscoverCard__sc-card___2YtVy'}):
            # Get all smallCase ID
            self.small_cases_id.append(a['id'])
            print(self.small_cases_id)
      except TimeoutException:
         # Try thrice and return
         print( "Timeout occurred" )

   def getSmallcaseList(self):
      content = self.driver.page_source
      soup = BeautifulSoup(content)
      for a in soup.findAll(attrs={'class':'DiscoverCard__sc-card___2YtVy'}):
         # Get all smallCase ID
         self.small_cases_id.append(a['id'])
         print(self.small_cases_id)

   def extractSmallCaseDetail(self):
      for id, id_value in enumerate(self.small_cases_id):
         small_case_id_uri = self.small_case_base_uri + id_value
         print(small_case_id_uri)
         driver.get(small_case_id_uri)
         content = driver.page_source
         soup = BeautifulSoup(content)
         print(soup)
         
if __name__ == "__main__":
   obj = ZerodhaLogin()
   obj.doLogin()
