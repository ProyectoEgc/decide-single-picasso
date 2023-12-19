# Generated by Selenium IDE
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from base.tests import BaseTestCase

import time
import os

class TestSelenium(StaticLiveServerTestCase):
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
  
  def test_WrongImport(self):
    self.driver.get(f'{self.live_server_url}/admin/census/census')
    self.driver.find_element(By.ID, "id_username").send_keys("miusuario")
    self.driver.find_element(By.ID, "id_password").send_keys("micontraseña")
    self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)

    self.driver.find_element(By.LINK_TEXT, "Censuss").click()
    self.driver.find_element(By.CSS_SELECTOR, ".import_link").click()
    DIR = os.path.dirname(os.path.realpath(__file__))
    archivo_relativo = 'static/WrongType.ods'
    archivo_absoluto = os.path.join(DIR, archivo_relativo)

    try:
      file_input = self.driver.find_element(By.ID, "id_import_file")
      file_input.send_keys(archivo_absoluto)
      time.sleep(3)
    except WebDriverException as e:
      print(f"Error al enviar teclas al elemento: {e}")

    dropdown = self.driver.find_element(By.ID, "id_input_format")
    dropdown.find_element(By.XPATH, "//option[. = 'xlsx']").click()
    self.driver.find_element(By.CSS_SELECTOR, ".default").click()    
    time.sleep(3)

  def test_EmptyImport(self):
    self.driver.get(f'{self.live_server_url}/admin/census/census')
    self.driver.find_element(By.ID, "id_username").send_keys("miusuario")
    self.driver.find_element(By.ID, "id_password").send_keys("micontraseña")
    self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)

    self.driver.find_element(By.LINK_TEXT, "Censuss").click()
    self.driver.find_element(By.CSS_SELECTOR, ".import_link").click()
    DIR = os.path.dirname(os.path.realpath(__file__))
    archivo_relativo = 'static/EmptyFile.xls'
    archivo_absoluto = os.path.join(DIR, archivo_relativo)

    try:
      file_input = self.driver.find_element(By.ID, "id_import_file")
      file_input.send_keys(archivo_absoluto)
      time.sleep(3)
    except WebDriverException as e:
      print(f"Error al enviar teclas al elemento: {e}")

    dropdown = self.driver.find_element(By.ID, "id_input_format")
    dropdown.find_element(By.XPATH, "//option[. = 'xlsx']").click()
    self.driver.find_element(By.CSS_SELECTOR, ".default").click()    
    time.sleep(3)

  def test_CorrectImport(self):
    self.driver.get(f'{self.live_server_url}/admin/census/census')
    self.driver.find_element(By.ID, "id_username").send_keys("miusuario")
    self.driver.find_element(By.ID, "id_password").send_keys("micontraseña")
    self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
    self.driver.find_element(By.LINK_TEXT, "Censuss").click()
    self.driver.find_element(By.CSS_SELECTOR, ".import_link").click()

    DIR = os.path.dirname(os.path.realpath(__file__))
    archivo_relativo = 'static/censoTestImport.xlsx'
    archivo_absoluto = os.path.join(DIR, archivo_relativo)

    try:
      file_input = self.driver.find_element(By.ID, "id_import_file")
      file_input.send_keys(archivo_absoluto)
      time.sleep(3)
    except WebDriverException as e:
      print(f"Error al enviar teclas al elemento: {e}")

    dropdown = self.driver.find_element(By.ID, "id_input_format")
    dropdown.find_element(By.XPATH, "//option[. = 'xlsx']").click()
    self.driver.find_element(By.CSS_SELECTOR, ".default").click()    
    time.sleep(3)
    self.driver.find_element(By.NAME, "confirm").click()
    time.sleep(3)





 
  
