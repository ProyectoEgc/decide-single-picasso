# Generated by Selenium IDE
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time

from base.tests import BaseTestCase
from selenium.webdriver.common.keys import Keys

class TestMultipleOptionVoting(StaticLiveServerTestCase):
    def setUp(self):
        # Configuración específica para Selenium y WebDriver
        options = webdriver.ChromeOptions()
        options.headless = False 
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

        # Configuración específica para Django y el cliente de prueba
        self.base = BaseTestCase()
        self.vars = {}
        self.base.setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()
        self.base.tearDown()

    def test_multiple_option_voting(self):
        self.login_as_admin()
        self.create_auth_for_multiple_voting()
        self.create_question_for_multiple_voting()
        self.create_multiple_voting()
        self.start_multiple_voting()

    def login_as_admin(self):
        self.driver.get(f"{self.live_server_url}/admin/login/?next=/admin/")
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").click()
        self.driver.find_element(By.ID, "id_password").send_keys("qwerty")
        self.driver.find_element(By.CSS_SELECTOR, ".submit-row > input").click()

    def create_auth_for_multiple_voting(self):
        self.driver.find_element(By.LINK_TEXT, "Auths").click()
        self.driver.find_element(By.CSS_SELECTOR, "li > .addlink").click()
        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys("test_auth")
        self.driver.find_element(By.ID, "id_url").click()
        self.driver.find_element(By.ID, "id_url").send_keys(self.live_server_url)
        self.driver.find_element(By.ID, "id_me").click()
        self.driver.find_element(By.NAME, "_save").click()

        success_message = self.driver.find_element(By.CSS_SELECTOR, ".success").text
        expected_message = f'El auth “{self.live_server_url}” fue agregado correctamente.'
        assert expected_message in success_message, f"Auth creation failed. Expected: {expected_message}, Actual: {success_message}"

    def create_question_for_multiple_voting(self):
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

        # Aserción para verificar que la pregunta se creó correctamente
        success_message = self.driver.find_element(By.CSS_SELECTOR, ".success").text
        expected_message = 'El question “pregunta de opcion multiple” fue agregado correctamente.'
        assert expected_message in success_message, f"Question creation failed. Expected: {expected_message}, Actual: {success_message}"

        
    def create_multiple_voting(self):
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
        
        # Aserción para verificar que la votación se creó correctamente
        success_message = self.driver.find_element(By.CSS_SELECTOR, ".success").text
        expected_message = 'El voting “votacion multiple” fue agregado correctamente.'
        assert expected_message in success_message, f"Voting creation failed. Expected: {expected_message}, Actual: {success_message}"


    def start_multiple_voting(self):
        self.driver.find_element(By.LINK_TEXT, "Votings").click()
        self.driver.find_element(By.NAME, "_selected_action").click()
        self.driver.find_element(By.NAME, "action").click()
        dropdown = self.driver.find_element(By.NAME, "action")
        dropdown.find_element(By.XPATH, "//option[. = 'Start']").click()
        self.driver.find_element(By.CSS_SELECTOR, "option:nth-child(3)").click()
        self.driver.find_element(By.NAME, "index").click()