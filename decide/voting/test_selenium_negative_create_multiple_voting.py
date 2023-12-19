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
from nose.tools import nottest

@nottest
class TestNegativeCreateMultipleVoting(StaticLiveServerTestCase):
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

    def test_multiple_option_voting(self):
        self.driver.get(f'{self.live_server_url}/admin/login/?next=/admin/')
        self.driver.find_element(By.ID,'id_username').send_keys("miusuario")
        self.driver.find_element(By.ID,'id_password').send_keys("micontraseña",Keys.ENTER)

        #Crea un usuario
        self.driver.find_element(By.LINK_TEXT, "Users").click()
        self.driver.find_element(By.CSS_SELECTOR, "li > .addlink").click()
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys("usuario1")
        self.driver.find_element(By.ID, "id_password1").click()
        self.driver.find_element(By.ID, "id_password1").send_keys("user1234")
        self.driver.find_element(By.ID, "id_password2").click()
        self.driver.find_element(By.ID, "id_password2").send_keys("user1234")
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
        self.driver.find_element(By.CSS_SELECTOR, "li > .addlink").click()
        self.driver.find_element(By.ID, "id_desc").send_keys("pregunta de opcion multiple")
        self.driver.find_element(By.ID, "id_type").click()
        dropdown = self.driver.find_element(By.ID, "id_type")
        dropdown.find_element(By.XPATH, "//option[. = 'Multiple options question']").click()
        self.driver.find_element(By.CSS_SELECTOR, "option:nth-child(3)").click()
        self.driver.find_element(By.ID, "id_options-0-option").click()
        self.driver.find_element(By.ID, "id_options-0-option").send_keys("a")
        self.driver.find_element(By.ID, "id_options-1-option").click()
        self.driver.find_element(By.ID, "id_options-1-option").send_keys("b")
        self.driver.find_element(By.ID, "id_options-2-option").click()
        self.driver.find_element(By.ID, "id_options-2-option").send_keys("c")
        self.driver.find_element(By.NAME, "_save").click()

        # Crear votacion
        self.driver.find_element(By.LINK_TEXT, "Votings").click()
        self.driver.find_element(By.CSS_SELECTOR, "li > .addlink").click()
        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys("votacion multiple")
        self.driver.find_element(By.ID, "id_desc").click()
        self.driver.find_element(By.ID, "id_desc").send_keys("votacion multiple")
        dropdown = self.driver.find_element(By.ID, "id_auths")
        dropdown.find_element(By.XPATH, f"//option[. = '{self.live_server_url}']").click()
        self.driver.find_element(By.ID, "id_question").click()
        dropdown = self.driver.find_element(By.ID, "id_question")
        dropdown.find_element(By.XPATH, "//option[. = 'pregunta de opcion multiple']").click()
        self.driver.find_element(By.CSS_SELECTOR, "#id_question > option:nth-child(2)").click()
        self.driver.find_element(By.NAME, "_save").click()
        # Añadir censo a la votación utilizando un usuario creado en BaseTestCase
        self.driver.find_element(By.LINK_TEXT, "Censuss").click()
        self.driver.find_element(By.CSS_SELECTOR, "li > .addlink").click()
        self.driver.find_element(By.ID, "id_voting_id").click()
        self.driver.find_element(By.ID, "id_voting_id").send_keys("8")
        self.driver.find_element(By.ID, "id_voter_id").click()
        self.driver.find_element(By.ID, "id_voter_id").send_keys("226")  # ID del usuario creado
        self.driver.find_element(By.NAME, "_save").click()
        time.sleep(25)
        # Iniciar votación
        self.driver.find_element(By.LINK_TEXT, "Votings").click()
        self.driver.find_element(By.NAME, "_selected_action").click()
        self.driver.find_element(By.NAME, "action").click()
        dropdown = self.driver.find_element(By.NAME, "action")
        dropdown.find_element(By.XPATH, "//option[. = 'Start']").click()
        self.driver.find_element(By.CSS_SELECTOR, "option:nth-child(3)").click()
        self.driver.find_element(By.NAME, "index").click()
        # El usuario censado accede a la votación
        
        self.driver.get(f"{self.live_server_url}/booth/8/")
        time.sleep(1)
        wait = WebDriverWait(self.driver, 10)
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".nav-item > .btn").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("usuario1")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("user1234")
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        time.sleep(2)
        # Validate the error message
        wait = WebDriverWait(self.driver, 10)
        error_message_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bi ~ div")))
        # Assert that the error message is displayed
        self.assertTrue(error_message_element.is_displayed(), "Error: Please select at least one option.")
