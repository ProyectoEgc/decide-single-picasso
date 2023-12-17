from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from base.tests import BaseTestCase
import time


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User

class TestSeleniumnegativecreatequestion(StaticLiveServerTestCase):
  def setUp(self):
    self.databases = 'test'
    self.base = BaseTestCase()
    self.base.setUp()
    options = webdriver.ChromeOptions()
    options.headless = False
    self.driver = webdriver.Chrome(options=options)

    self.user = User.objects.create_user(username='miusuario', password='micontraseña')
    self.user.is_staff = True
    self.user.is_superuser = True
    self.user.save()
    super().setUp()            
          
  def tearDown(self):           
    super().tearDown()
    self.driver.quit()
    self.base.tearDown()
  
  def test_seleniumnegativecreatequestion(self):
    self.driver.get(f'{self.live_server_url}/admin/')
    self.driver.find_element(By.ID,'id_username').send_keys("miusuario")
    self.driver.find_element(By.ID,'id_password').send_keys("micontraseña",Keys.ENTER)
    self.assertTrue(len(self.driver.find_elements(By.ID, 'user-tools'))==1)
    time.sleep(2)
    self.driver.find_element(By.LINK_TEXT, "Questions").click()
    self.driver.find_element(By.CSS_SELECTOR, "li > .addlink").click()
    self.driver.find_element(By.ID, "id_options-0-option").click()
    self.driver.find_element(By.ID, "id_options-0-option").send_keys("no valido")
    self.driver.find_element(By.ID, "id_options-1-option").click()
    self.driver.find_element(By.ID, "id_options-1-option").send_keys("no valido")
    self.driver.find_element(By.ID, "id_options-2-option").click()
    self.driver.find_element(By.ID, "id_options-2-option").send_keys("no valido")
    self.driver.find_element(By.NAME, "_save").click()
    time.sleep(5)
    wait = WebDriverWait(self.driver, 10)
    error_message_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".errorlist li")))
    # Assert that the error message is displayed
    self.assertTrue(error_message_element.is_displayed(), "Por favor corrija el siguiente error.")
