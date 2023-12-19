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

class AdminTestCase(StaticLiveServerTestCase):

  def setUp(self):
    self.base = BaseTestCase()
    self.base.setUp()
    options = webdriver.ChromeOptions()
    options.headless = True
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
  
  def test_simpleCorrectLogin(self):               
    self.driver.get(f'{self.live_server_url}/admin/login/?next=/admin/')
    self.driver.find_element(By.ID,'id_username').send_keys("miusuario")
    self.driver.find_element(By.ID,'id_password').send_keys("micontraseña",Keys.ENTER)
    time.sleep(1)
    self.driver.find_element(By.LINK_TEXT, "Users").click()
    time.sleep(1)
    self.driver.find_element(By.CSS_SELECTOR, "li > .addlink").click()
    time.sleep(1)
    self.driver.find_element(By.ID, "id_username").click()
    time.sleep(1)
    self.driver.find_element(By.ID, "id_username").send_keys("usuarionormal")

    self.driver.find_element(By.ID, "id_password1").click()
    self.driver.find_element(By.ID, "id_password1").send_keys("user1234")
    self.driver.find_element(By.ID, "id_password2").click()
    self.driver.find_element(By.ID, "id_password2").send_keys("user1234")
    self.driver.find_element(By.NAME, "_save").click()
    

      
  

