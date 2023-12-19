# Generated by Selenium IDE
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support import expected_conditions as EC

class TestRegister(StaticLiveServerTestCase):
  def setUp(self):
    options = webdriver.ChromeOptions()
    options.headless = False 
    self.driver = webdriver.Chrome(options=options)

    super().setUp()

  def teardown_method(self, method):
    super().tearDown()
    self.driver.quit()
  
  def test_register(self):
    self.driver.get(f"{self.live_server_url}/signup/")
    self.driver.find_element(By.ID, "username").click()
    self.driver.find_element(By.ID, "username").send_keys("test")
    self.driver.find_element(By.ID, "first_name").click()
    self.driver.find_element(By.ID, "first_name").send_keys("test")
    self.driver.find_element(By.ID, "last_name").click()
    self.driver.find_element(By.ID, "last_name").send_keys("test")
    self.driver.find_element(By.ID, "email").click()
    self.driver.find_element(By.ID, "email").send_keys("test@gmail.com")
    self.driver.find_element(By.ID, "password1").click()
    self.driver.find_element(By.ID, "password1").send_keys("test")
    self.driver.find_element(By.ID, "password2").click()
    self.driver.find_element(By.ID, "password2").send_keys("test")
    self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
    
    # Verificar que la URL se redirige correctamente después del registro
    expected_login_url = f"{self.live_server_url}/authentication/login-view/"
    current_url = self.driver.current_url
    self.assertEqual(current_url, expected_login_url, f"La URL actual {current_url} no coincide con la esperada {expected_login_url}")


  def test_negative_register(self):
    self.driver.get(f"{self.live_server_url}/signup/")
    self.driver.find_element(By.ID, "username").click()
    self.driver.find_element(By.ID, "username").send_keys("test")
    self.driver.find_element(By.ID, "first_name").click()
    self.driver.find_element(By.ID, "first_name").send_keys("test")
    self.driver.find_element(By.ID, "last_name").click()
    self.driver.find_element(By.ID, "last_name").send_keys("test")
    self.driver.find_element(By.ID, "email").click()
    self.driver.find_element(By.ID, "email").send_keys("test@gmail.com")
    self.driver.find_element(By.ID, "password1").click()
    self.driver.find_element(By.ID, "password1").send_keys("test1")
    self.driver.find_element(By.ID, "password2").click()
    self.driver.find_element(By.ID, "password2").send_keys("test2")
    self.driver.find_element(By.CSS_SELECTOR, ".btn").click() 

    error_message_locator = (By.CSS_SELECTOR, ".alert")  # Reemplaza con el selector real
    WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(error_message_locator))

    error_message_element = self.driver.find_element(*error_message_locator)
    assert "Passwords do not match" in error_message_element.text, "Mensaje de error incorrecto"