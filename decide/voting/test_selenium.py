# Generated by Selenium IDE
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.keys import Keys
from base.tests import BaseTestCase
from selenium.common.exceptions import NoSuchElementException
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

from django.contrib.auth.models import User

class TestImageVoting(StaticLiveServerTestCase):
  def setUp(self):
    # Configuración específica para Selenium y WebDriver
    options = webdriver.ChromeOptions()
    options.headless = True 

    self.driver = webdriver.Chrome(options=options)

    self.user = User.objects.create_user(username='miusuario', password='micontraseña')
    self.user.is_staff = True
    self.user.is_superuser = True
    self.user.save()

    super().setUp()

    # Configuración específica para Django y el cliente de prueba
    self.base = BaseTestCase()
    self.vars = {}
    self.base.setUp()    
       
          
  def tearDown(self):           
    super().tearDown()
    self.driver.quit()

    self.base.tearDown()

  def testimageQuestionSuccess(self):
    self.driver.get(f'{self.live_server_url}/admin/')
    self.driver.set_window_size(1210, 773)
    self.driver.find_element(By.ID, "id_username").click()
    self.driver.find_element(By.ID, "id_username").send_keys("miusuario")
    self.driver.find_element(By.ID, "id_password").send_keys("micontraseña")
    self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
    self.driver.find_element(By.LINK_TEXT, "Questions").click()
    self.driver.find_element(By.CSS_SELECTOR, "li > .addlink").click()

    self.driver.find_element(By.ID, "id_desc").click()
    self.driver.find_element(By.ID, "id_desc").send_keys("Pregunta imagenes")
    dropdown = self.driver.find_element(By.ID, "id_type")
    dropdown.find_element(By.XPATH, "//option[. = 'Image question']").click()
        
    self.driver.find_element(By.ID, "id_options-0-number").click()
    self.driver.find_element(By.ID, "id_options-0-number").send_keys("1")
    self.driver.find_element(By.ID, "id_options-0-option").click()
    self.driver.find_element(By.ID, "id_options-0-option").send_keys("Imagen 1")
        
    try:
        DIR = os.path.dirname(os.path.realpath(__file__))
        archivo_relativo = 'static/1.jpeg'
        archivo_absoluto = os.path.join(DIR, archivo_relativo)
        file_input = self.driver.find_element(By.ID, "id_options-0-image")
        file_input.send_keys(archivo_absoluto) 
        time.sleep(1)
    except WebDriverException as e:
        print(f"Error al enviar teclas al elemento: {e}")

    self.driver.find_element(By.ID, "id_options-1-number").click()
    self.driver.find_element(By.ID, "id_options-1-number").send_keys("2")
    self.driver.find_element(By.ID, "id_options-1-option").click()
    self.driver.find_element(By.ID, "id_options-1-option").send_keys("Imagen 2")

    try:
        DIR = os.path.dirname(os.path.realpath(__file__))
        archivo_relativo = 'static/2.jpeg'
        archivo_absoluto = os.path.join(DIR, archivo_relativo)
        file_input = self.driver.find_element(By.ID, "id_options-1-image")
        file_input.send_keys(archivo_absoluto)
        time.sleep(1)
    except WebDriverException as e:
        print(f"Error al enviar teclas al elemento: {e}")
       
    self.driver.find_element(By.NAME, "_save").click()
    time.sleep(2)
  
  