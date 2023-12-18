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

class TestPositiveCreateYesNoQuestion(StaticLiveServerTestCase):
    def setUp(self):
        # Configuración del entorno de pruebas
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
        # Limpieza después de las pruebas
        super().tearDown()
        self.driver.quit()
        self.base.tearDown()

    def test_positive_create_yes_no_question(self):
        # Navegar al panel de administración e iniciar sesión
        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element(By.ID, 'id_username').send_keys("miusuario")
        self.driver.find_element(By.ID, 'id_password').send_keys("micontraseña", Keys.ENTER)
        self.assertTrue(len(self.driver.find_elements(By.ID, 'user-tools')) == 1)
        time.sleep(2)

        # Ir a la sección de preguntas
        self.driver.find_element(By.LINK_TEXT, "Questions").click()

        # Crear una nueva pregunta de tipo yes/no con opciones válidas
        self.driver.find_element(By.CSS_SELECTOR, "li > .addlink").click()
        self.driver.find_element(By.ID, "id_desc").send_keys("pregunta yes/no válida")
        self.driver.find_element(By.ID, "id_type").click()
        dropdown = self.driver.find_element(By.ID, "id_type")
        dropdown.find_element(By.XPATH, "//option[. = 'Yes/No question']").click()
        self.driver.find_element(By.CSS_SELECTOR, "option:nth-child(2)").click()

        # Agregar opciones válidas a la pregunta yes/no ('Sí' y 'No')
        option_input = self.driver.find_element(By.ID, "id_options-0-option")
        option_input.click()
        option_input.send_keys("Sí")
        
        option_input = self.driver.find_element(By.ID, "id_options-1-option")
        option_input.click()
        option_input.send_keys("No")

        self.driver.find_element(By.NAME, "_save").click()
        time.sleep(5)

        # Verificar que la pregunta fue creada exitosamente sin mostrar mensajes de error
        success_message_element = self.driver.find_element(By.CSS_SELECTOR, ".success")
        self.assertTrue(success_message_element.is_displayed(), "La pregunta yes/no se creó con éxito.")

