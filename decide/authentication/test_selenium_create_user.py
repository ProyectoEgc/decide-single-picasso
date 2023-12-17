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
    self.databases = 'test'
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
    self.driver.get(f'{self.live_server_url}/admin/')
    self.driver.find_element(By.ID,'id_username').send_keys("miusuario")
    self.driver.find_element(By.ID,'id_password').send_keys("micontraseña",Keys.ENTER)
    #Verifica que nos hemos logado porque aparece la barra de herramientas superior
    self.assertTrue(len(self.driver.find_elements(By.ID, 'user-tools'))==1)
    self.driver.find_element(By.LINK_TEXT, "Usuarios").click()
    time.sleep(5)
    self.driver.find_element(By.CSS_SELECTOR, "li > .addlink").click()
    self.driver.find_element(By.ID, "id_username").click()
    self.driver.find_element(By.ID, "id_username").send_keys("usuario1")
    self.driver.find_element(By.ID, "id_password1").click()
    self.driver.find_element(By.ID, "id_password1").send_keys("user1234")
    self.driver.find_element(By.ID, "id_password2").click()
    self.driver.find_element(By.ID, "id_password2").send_keys("user1234")
    self.driver.find_element(By.NAME, "_save").click()
    time.sleep(5)
    wait = WebDriverWait(self.driver, 10)
    success_message_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".messagelist .success")))  
    # Assert that the error message is displayed
    self.assertTrue(success_message_element.is_displayed(), "El usuario 'usuario1' se ha agregado correctamente. Puede editarlo nuevamente a continuación.")
      
  

