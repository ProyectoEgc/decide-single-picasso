# Generated by Selenium IDE
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.keys import Keys
from base.tests import BaseTestCase
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
  
  def testIMageVoting(self):

    # Iniciar sesion como admin
    self.driver.get(f'{self.live_server_url}/admin/')
    self.driver.set_window_size(1210, 773)

    self.driver.find_element(By.ID, "id_username").send_keys("miusuario")
    self.driver.find_element(By.ID, "id_password").send_keys("micontraseña")
    self.driver.find_element(By.CSS_SELECTOR, ".submit-row > input").click()

    # Crear usuario, no necesario
    self.driver.find_element(By.LINK_TEXT, "Usuarios").click()
    
    #Numero para controlar la id del usuario para usarla en el censo
    numero_usuarios = self.driver.find_element(By.CLASS_NAME,"paginator")
    texto = numero_usuarios.text
    numero_usuarios = ''.join(filter(str.isdigit, texto))
    numero = int(numero_usuarios)
    numero += 1
    
    username = "Usuario" + str(numero)
    password = "@Hola123"
    
    self.driver.find_element(By.CSS_SELECTOR, "li > .addlink").click()
    self.driver.find_element(By.ID, "id_username").click()
    self.driver.find_element(By.ID, "id_username").send_keys(username)
    self.driver.find_element(By.ID, "id_password1").click()
    self.driver.find_element(By.ID, "id_password1").send_keys(password)
    self.driver.find_element(By.ID, "id_password2").click()
    self.driver.find_element(By.ID, "id_password2").send_keys(password)
    self.driver.find_element(By.NAME, "_save").click()

    # Crear auth para la votacion
    self.driver.find_element(By.LINK_TEXT, "Auths").click()
    self.driver.find_element(By.CSS_SELECTOR, "li > .addlink").click()
    self.driver.find_element(By.ID, "id_name").click()
    self.driver.find_element(By.ID, "id_name").send_keys("test_auth")
    self.driver.find_element(By.ID, "id_url").click()
    self.driver.find_element(By.ID, "id_url").send_keys(f'{self.live_server_url}')
    self.driver.find_element(By.ID, "id_me").click()
    self.driver.find_element(By.NAME, "_save").click()

    # Crear question para la votacion
    self.driver.find_element(By.LINK_TEXT, "Questions").click()
      
    numero_usuarios = self.driver.find_element(By.CLASS_NAME,"paginator")
    texto = numero_usuarios.text
    
    #Número para pasar como parámetro a la hora de eleigir la question en la votación
    numero_questions = ''.join(filter(str.isdigit, texto))
    numero_q = int(numero_questions)
    numero_q += 2
    
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


    # Crear votacion
    self.driver.find_element(By.LINK_TEXT, "Votings").click()
    
    numero_usuarios = self.driver.find_element(By.CLASS_NAME,"paginator")
    texto = numero_usuarios.text
    
    #Número para tener de voting id
    numero_questions = ''.join(filter(str.isdigit, texto))
    numero_v = int(numero_questions)
    numero_v += 1
    
    self.driver.find_element(By.CSS_SELECTOR, "li > .addlink").click()
    self.driver.find_element(By.ID, "id_name").click()
    
    nombre_votacion = "Votacion Imagenes" + str(numero)
    
    self.driver.find_element(By.ID, "id_name").send_keys(nombre_votacion)
    self.driver.find_element(By.ID, "id_desc").click()
    self.driver.find_element(By.ID, "id_desc").send_keys("Votacion Imagenes")
    dropdown = self.driver.find_element(By.ID, "id_auths")
    dropdown.find_element(By.XPATH, f"//option[. = '{self.live_server_url}']").click()
    self.driver.find_element(By.ID, "id_question").click()
    dropdown = self.driver.find_element(By.ID, "id_question")
    
    dropdown.find_element(By.XPATH, "//option[. = 'Pregunta imagenes']").click()    
    self.driver.find_element(By.CSS_SELECTOR, "#id_question > option:nth-child(2)").click()
    self.driver.find_element(By.NAME, "_save").click()

    # Iniciar votacion
    self.driver.find_element(By.NAME, "_selected_action").click()
    self.driver.find_element(By.NAME, "action").click()
    dropdown = self.driver.find_element(By.NAME, "action")
    dropdown.find_element(By.XPATH, "//option[. = 'Start']").click()    
    self.driver.find_element(By.CSS_SELECTOR, "option:nth-child(3)").click()
    self.driver.find_element(By.NAME, "index").click()
    
    # Añadir censo a la votacion
        
    self.driver.find_element(By.LINK_TEXT, "Censuss").click()
    self.driver.find_element(By.CSS_SELECTOR, "li > .addlink").click()
    self.driver.find_element(By.ID, "id_voting_id").click()
    self.driver.find_element(By.ID, "id_voting_id").send_keys(numero_v)
    self.driver.find_element(By.ID, "id_voter_id").click()
    self.driver.find_element(By.ID, "id_voter_id").send_keys(numero)
    self.driver.find_element(By.NAME, "_save").click()

    
    # El usuario censado accede a la votacion
    
    # Puedes cambiar este valor según tus necesidades
    self.driver.get(f'{self.live_server_url}/booth/{numero_v}')
    time.sleep(2)
    self.driver.find_element(By.CSS_SELECTOR, ".nav-item > .btn").click()
    self.driver.find_element(By.ID, "username").click()
    self.driver.find_element(By.ID, "username").send_keys(username)
    self.driver.find_element(By.ID, "password").click()
    self.driver.find_element(By.ID, "password").send_keys(password)
    self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    time.sleep(2)
    self.driver.find_element(By.ID, "q1").click()


    



