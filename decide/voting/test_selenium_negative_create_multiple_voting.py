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
from selenium.webdriver.common.action_chains import ActionChains


class TestSeleniumnegativecreatemultiplevoting(StaticLiveServerTestCase):
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
  
  def test_seleniumnegativecreatemultiplevoting(self):
    self.driver.get(f'{self.live_server_url}/admin/')
    self.driver.find_element(By.ID,'id_username').send_keys("miusuario")
    self.driver.find_element(By.ID,'id_password').send_keys("micontraseña",Keys.ENTER)
    self.driver.find_element(By.LINK_TEXT, "Questions").click()
    self.driver.find_element(By.CSS_SELECTOR, "li > .addlink").click()
    self.driver.find_element(By.ID, "id_desc").send_keys("test multiple option question")
    dropdown = self.driver.find_element(By.ID, "id_type")
    dropdown.find_element(By.XPATH, "//option[. = 'Multiple options question']").click()
    element = self.driver.find_element(By.ID, "id_type")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    element = self.driver.find_element(By.ID, "id_type")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.ID, "id_type")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    self.driver.find_element(By.ID, "id_options-0-option").click()
    self.driver.find_element(By.ID, "id_options-0-option").send_keys("not mark")
    self.driver.find_element(By.ID, "id_options-1-option").click()
    self.driver.find_element(By.ID, "id_options-1-option").send_keys("not mark")
    self.driver.find_element(By.ID, "id_options-2-option").click()
    self.driver.find_element(By.ID, "id_options-2-option").send_keys("not mark")
    self.driver.find_element(By.NAME, "_save").click()
    self.driver.find_element(By.LINK_TEXT, "Votings").click()
    self.driver.find_element(By.CSS_SELECTOR, "li > .addlink").click()
    self.driver.find_element(By.ID, "id_name").send_keys("test multiple voting")
    self.driver.find_element(By.ID, "id_desc").click()
    self.driver.find_element(By.ID, "id_desc").click()
    self.driver.find_element(By.ID, "id_desc").send_keys("this is a negative multiple voting")
    dropdown = self.driver.find_element(By.ID, "id_question")
    dropdown.find_element(By.XPATH, "//option[. = 'test multiple option question']").click()
    element = self.driver.find_element(By.ID, "id_question")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    element = self.driver.find_element(By.ID, "id_question")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.ID, "id_question")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    time.sleep(3)
    self.vars["window_handles"] = self.driver.window_handles
    time.sleep(3)
    self.driver.find_element(By.CSS_SELECTOR, "#add_id_auths > img").click()
    time.sleep(3)
    self.vars["win3530"] = self.wait_for_window(2000)
    time.sleep(3)
    self.vars["root"] = self.driver.current_window_handle
    time.sleep(3)
    self.driver.switch_to.window(self.vars["win3530"])
    time.sleep(3)
    self.driver.find_element(By.ID, "id_name").click()
    self.driver.find_element(By.ID, "id_name").send_keys("http://localhost:8080")
    self.driver.find_element(By.ID, "id_url").click()
    self.driver.find_element(By.ID, "id_url").send_keys("http://localhost:8080")
    self.driver.find_element(By.ID, "id_me").click()
    self.driver.find_element(By.NAME, "_save").click()
    self.driver.close()
    self.driver.switch_to.window(self.vars["root"])
    self.driver.find_element(By.NAME, "_save").click()
    self.driver.find_element(By.LINK_TEXT, "Censuss").click()
    self.driver.find_element(By.CSS_SELECTOR, "li > .addlink").click()
    self.driver.find_element(By.ID, "id_voting_id").send_keys("1")
    self.driver.find_element(By.ID, "id_voter_id").click()
    self.driver.find_element(By.ID, "id_voter_id").send_keys("2")
    self.driver.find_element(By.NAME, "_save").click()
    self.driver.find_element(By.CSS_SELECTOR, ".model-voting > th").click()
    self.driver.find_element(By.LINK_TEXT, "Votings").click()
    self.driver.find_element(By.NAME, "_selected_action").click()
    dropdown = self.driver.find_element(By.NAME, "action")
    dropdown.find_element(By.XPATH, "//option[. = 'Start']").click()
    element = self.driver.find_element(By.NAME, "action")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    element = self.driver.find_element(By.NAME, "action")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.NAME, "action")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    self.driver.find_element(By.NAME, "index").click()
    self.driver.find_element(By.ID, "username").send_keys("decide")
    self.driver.find_element(By.ID, "password").send_keys("decide")
    self.driver.find_element(By.CSS_SELECTOR, ".nav-item > .btn").click()
    self.driver.find_element(By.ID, "registerModal").click()
    self.driver.find_element(By.ID, "username").send_keys("usuario1")
    self.driver.find_element(By.ID, "registerModal").click()
    self.driver.find_element(By.ID, "password").send_keys("user1234")
    self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    element = self.driver.find_element(By.CSS_SELECTOR, ".btn-primary")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element, 0, 0).perform()
  
