import os
import random
import itertools
import time
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from selenium.common.exceptions import WebDriverException
from django.core.exceptions import ValidationError


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from base import mods
from base.tests import BaseTestCase
from census.models import Census
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption
from datetime import datetime


class VotingTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def create_voting(self):
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    def create_voters(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user

    def store_votes(self, v):
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()

        clear = {}
        for opt in v.question.options.all():
            clear[opt.number] = 0
            for i in range(random.randint(0, 5)):
                a, b = self.encrypt_msg(opt.number, v)
                data = {
                    'voting': v.id,
                    'voter': voter.voter_id,
                    'vote': { 'a': a, 'b': b },
                }
                clear[opt.number] += 1
                user = self.get_or_create_user(voter.voter_id)
                self.login(user=user.username)
                voter = voters.pop()
                mods.post('store', json=data)
        return clear

    def test_complete_voting(self):
        v = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes(v)

        self.login()  # set token
        v.tally_votes(self.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])

    def test_create_voting_from_api(self):
        data = {'name': 'Example'}
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'I want a ',
            'question_opt': ['cat', 'dog', 'horse'],
            'image': 'Image.jpeg'
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_voting(self):
        voting = self.create_voting()

        data = {'action': 'start'}
        #response = self.client.post('/voting/{}/'.format(voting.pk), data, format='json')
        #self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        data = {'action': 'bad'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)

        # STATUS VOTING: not started
        for action in ['stop', 'tally']:
            data = {'action': action}
            response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), 'Voting is not started')

        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting started')

        # STATUS VOTING: started
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting is not stopped')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting stopped')

        # STATUS VOTING: stopped
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting tallied')

        # STATUS VOTING: tallied
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already tallied')

    def test_create_voting_API(self):
        self.login()
        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'I want a ',
            'question_opt': ['cat', 'dog', 'horse'],
            'image': 'Image.jpeg'
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

        voting = Voting.objects.get(name='Example')
        self.assertEqual(voting.desc, 'Description example')

    def test_create_score_question(self):
        q = Question(desc='Score question test', type='S')
        q.save()
        self.assertEquals(len(q.options.all()), 11)
        self.assertEquals(q.type, 'S')
        for i in range(0, 11):
            if(i==0):
                self.assertEquals(q.options.all()[i].option, str(i))
            else:
                self.assertEquals(q.options.all()[i].option, str(i))

    def test_empty_description(self):
        with self.assertRaises(ValidationError):
            question = Question(desc='')  
            question.full_clean()  


    def test_create_score_question_creating_other_options(self):
        q = Question(desc='Score question test', type='S')
        q.save()

        q01=QuestionOption(question= q, option = "Probando")
        q01.save()
        q02=QuestionOption(question= q, option = "Seguimos probando")
        q02.save()
        q03=QuestionOption(question= q, option = "Creando preguntas")
        q03.save()
        q04=QuestionOption(question= q, option = "Para")
        q04.save()
        q05=QuestionOption(question= q, option = "Tests")
        q05.save()

        q.save()
        self.assertEquals(len(q.options.all()), 11)
        self.assertEquals(q.type, 'S')

        for i in range(0, 11):
            if(i==0):
                self.assertEquals(q.options.all()[i].option, str(i))

            else:
                self.assertEquals(q.options.all()[i].option, str(i))

    def test_update_voting_405(self):
        v = self.create_voting()
        data = {} #El campo action es requerido en la request
        self.login()
        response = self.client.post('/voting/{}/'.format(v.pk), data, format= 'json')
        self.assertEquals(response.status_code, 405)
    
    def test_to_string(self):
        #Crea un objeto votacion
        v = self.create_voting()
        #Verifica que el nombre de la votacion es test voting
        self.assertEquals(str(v),"test voting")
        #Verifica que la descripcion de la pregunta sea test question
        self.assertEquals(str(v.question),"test question")
        #Verifica que la primera opcion es option1 (2)
        self.assertEquals(str(v.question.options.all()[0]),"option 1 (2)")

    # Testing yes/no question feature
    def test_create_image_question(self):
        q = Question(desc='Image', type='I')
        q.save()

        q01 = QuestionOption(question = q, option = "First option", image = 'Image.jpeg')
        q01.save()
        q02 = QuestionOption(question = q, option = "Second option", image = 'Image.jpeg')
        q02.save()
        q03 = QuestionOption(question = q, option = "Third option", image = 'Image.jpeg')
        q03.save()

        self.assertEquals(q.options.all().count(), 3)
        self.assertEquals(q.type, 'I')
        self.assertEquals(q.options.all()[0].option, 'First option')
        self.assertEquals(q.options.all()[1].option, 'Second option')
        self.assertEquals(q.options.all()[2].option, 'Third option')
        self.assertEquals(q.options.all()[0].number, 2)
        self.assertEquals(q.options.all()[1].number, 3)
        self.assertEquals(q.options.all()[2].number, 4)

    # Testing yes/no question feature
    def test_create_yes_no_question(self):
        q = Question(desc='Yes/No question test', type='B')
        q.save()

        self.assertEquals(q.options.all().count(), 2)
        self.assertEquals(q.type, 'B')
        self.assertEquals(q.options.all()[0].option, 'Sí')
        self.assertEquals(q.options.all()[1].option, 'No')
        self.assertEquals(q.options.all()[0].number, 1)
        self.assertEquals(q.options.all()[1].number, 2)

    # Adding options other than yes and no manually
    def test_create_yes_no_question_with_other_options(self):
        q = Question(desc='Yes/No question test', type='B')
        q.save()
        qo1 = QuestionOption(question = q, option = 'First option')
        qo1.save()
        qo2 = QuestionOption(question = q, option = 'Second option')
        qo2.save()
        qo3 = QuestionOption(question = q, option = 'Third option')
        qo3.save()

        self.assertEquals(q.options.all().count(), 2)
        self.assertEquals(q.type, 'B')
        self.assertEquals(q.options.all()[0].option, 'Sí')
        self.assertEquals(q.options.all()[1].option, 'No')
        self.assertEquals(q.options.all()[0].number, 1)
        self.assertEquals(q.options.all()[1].number, 2)

    # Updating options yes no
    def test_update_yes_no_question_without_additional_options(self):
        # Crear una pregunta de sí/no inicialmente
        q = Question(desc='Yes/No question test', type='B')
        q.save()

        # Verificar que la pregunta se creó correctamente como sí/no
        self.assertEqual(q.options.all().count(), 2)
        self.assertEqual(q.type, 'B')
        self.assertEqual(q.options.all()[0].option, 'Sí')
        self.assertEqual(q.options.all()[1].option, 'No')
        self.assertEqual(q.options.all()[0].number, 1)
        self.assertEqual(q.options.all()[1].number, 2)

        # Actualizar la pregunta sin agregar opciones adicionales
        q.desc = 'Updated Yes/No question test'
        q.save()

        # Verificar que la pregunta se actualizó correctamente y aún tiene solo dos opciones (Sí/No)
        self.assertEqual(q.options.all().count(), 2)
        self.assertEqual(q.type, 'B')
        self.assertEqual(q.options.all()[0].option, 'Sí')
        self.assertEqual(q.options.all()[1].option, 'No')
        self.assertEqual(q.options.all()[0].number, 1)
        self.assertEqual(q.options.all()[1].number, 2)
    
    # Updating options yes no with additional options
    def test_update_yes_no_question_with_additional_options(self):
        # Crear una pregunta de sí/no inicialmente
        q = Question(desc='Yes/No question test', type='B')
        q.save()
        qo1 = QuestionOption(question = q, option = 'First option')
        qo1.save()
        qo2 = QuestionOption(question = q, option = 'Second option')
        qo2.save()
        qo3 = QuestionOption(question = q, option = 'Third option')
        qo3.save()

        # Verificar que la pregunta se creó correctamente como sí/no
        self.assertEqual(q.options.all().count(), 2)
        self.assertEqual(q.type, 'B')
        self.assertEqual(q.options.all()[0].option, 'Sí')
        self.assertEqual(q.options.all()[1].option, 'No')
        self.assertEqual(q.options.all()[0].number, 1)
        self.assertEqual(q.options.all()[1].number, 2)

        # Actualizar la pregunta sin agregar opciones adicionales
        q.desc = 'Updated Yes/No question test'
        q.save()
        qo1 = QuestionOption(question = q, option = 'First option')
        qo1.save()
        qo2 = QuestionOption(question = q, option = 'Second option')
        qo2.save()
        qo3 = QuestionOption(question = q, option = 'Third option')
        qo3.save()

        # Verificar que la pregunta se actualizó correctamente y aún tiene solo dos opciones (Sí/No)
        self.assertEqual(q.options.all().count(), 2)
        self.assertEqual(q.type, 'B')
        self.assertEqual(q.options.all()[0].option, 'Sí')
        self.assertEqual(q.options.all()[1].option, 'No')
        self.assertEqual(q.options.all()[0].number, 1)
        self.assertEqual(q.options.all()[1].number, 2)

    def test_delete_yes_no_question_and_options(self):
        # Crear una pregunta de sí/no
        q = Question(desc='Yes/No question test', type='B')
        q.save()

        # Agregar opciones adicionales a la pregunta de sí/no
        qo1 = QuestionOption(question=q, option='First option')
        qo1.save()
        qo2 = QuestionOption(question=q, option='Second option')
        qo2.save()

        # Verificar que la pregunta tiene las opciones originales
        self.assertEqual(q.options.all().count(), 2) 

        # Eliminar la pregunta de sí/no
        q.delete()

        # Verificar que la pregunta y sus opciones asociadas fueron eliminadas correctamente
        self.assertFalse(Question.objects.filter(desc='Yes/No question test').exists())  # Verificar que la pregunta fue eliminada
        self.assertFalse(QuestionOption.objects.filter(question=q).exists())  # Verificar que las opciones fueron eliminadas


    # Testing multiple option question feature
    def test_create_multiple_options_question_without_numbers(self):
        q = Question(desc='Multiple option question test', type='m')
        q.save()

        qo1 = QuestionOption(question = q, option = 'First option')
        qo1.save()
        qo2 = QuestionOption(question = q, option = 'Second option')
        qo2.save()
        qo3 = QuestionOption(question = q, option = 'Third option')
        qo3.save()

        self.assertEquals(q.type, 'm')
        self.assertEquals(q.options.all()[0].option, 'First option')
        self.assertEquals(q.options.all()[1].option, 'Second option')
        self.assertEquals(q.options.all()[2].option, 'Third option')
        self.assertEquals(q.options.all()[0].number, 2)
        self.assertEquals(q.options.all()[1].number, 3)
        self.assertEquals(q.options.all()[2].number, 4)

    # Testing multiple option question with more than 3 options feature
    def test_create_multiple_options_question_with_numbers_and_more_than_3_options(self):
        q = Question(desc='Multiple option question test', type='m')
        q.save()

        qo1 = QuestionOption(question = q, number = 1,option = 'First option')
        qo1.save()
        qo2 = QuestionOption(question = q, number = 2,option = 'Second option')
        qo2.save()
        qo3 = QuestionOption(question = q, number = 3,option = 'Third option')
        qo3.save()
        qo4 = QuestionOption(question = q, number = 4,option = 'Fourth option')
        qo4.save()
        qo5 = QuestionOption(question = q, number = 5,option = 'Fifth option')
        qo5.save()

        self.assertEquals(q.type, 'm')
        self.assertEquals(q.options.all()[0].option, 'First option')
        self.assertEquals(q.options.all()[1].option, 'Second option')
        self.assertEquals(q.options.all()[2].option, 'Third option')
        self.assertEquals(q.options.all()[3].option, 'Fourth option')
        self.assertEquals(q.options.all()[4].option, 'Fifth option')
        self.assertEquals(q.options.all()[0].number, 1)
        self.assertEquals(q.options.all()[1].number, 2)
        self.assertEquals(q.options.all()[2].number, 3)
        self.assertEquals(q.options.all()[3].number, 4)
        self.assertEquals(q.options.all()[4].number, 5)

class LogInSuccessTests(StaticLiveServerTestCase):

    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def successLogIn(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)

        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")
        self.assertTrue(self.cleaner.current_url == self.live_server_url+"/admin/")

class LogInErrorTests(StaticLiveServerTestCase):

    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def usernameWrongLogIn(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)
        
        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("usuarioNoExistente")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("usuarioNoExistente")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")

        self.assertTrue(self.cleaner.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/p').text == 'Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive.')

    def passwordWrongLogIn(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)

        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("wrongPassword")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")

        self.assertTrue(self.cleaner.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/p').text == 'Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive.')

class QuestionsTests(StaticLiveServerTestCase):

    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()
        self.cleaner = Cleaner() 

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()
    
    def createQuestionSuccess(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)

        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")

        self.cleaner.get(self.live_server_url+"/admin/voting/question/add/")
        
        self.cleaner.find_element(By.ID, "id_desc").click()
        self.cleaner.find_element(By.ID, "id_desc").send_keys('Test')
        self.cleaner.find_element(By.ID, "id_options-0-number").click()
        self.cleaner.find_element(By.ID, "id_options-0-number").send_keys('1')
        self.cleaner.find_element(By.ID, "id_options-0-option").click()
        self.cleaner.find_element(By.ID, "id_options-0-option").send_keys('test1')
        self.cleaner.find_element(By.ID, "id_options-1-number").click()
        self.cleaner.find_element(By.ID, "id_options-1-number").send_keys('2')
        self.cleaner.find_element(By.ID, "id_options-1-option").click()
        self.cleaner.find_element(By.ID, "id_options-1-option").send_keys('test2')
        self.cleaner.find_element(By.NAME, "_save").click()

        self.assertTrue(self.cleaner.current_url == self.live_server_url+"/admin/voting/question/")

    def createCensusEmptyError(self):
        self.cleaner.get(self.live_server_url+"/admin/login/?next=/admin/")
        self.cleaner.set_window_size(1280, 720)

        self.cleaner.find_element(By.ID, "id_username").click()
        self.cleaner.find_element(By.ID, "id_username").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").click()
        self.cleaner.find_element(By.ID, "id_password").send_keys("decide")

        self.cleaner.find_element(By.ID, "id_password").send_keys("Keys.ENTER")

        self.cleaner.get(self.live_server_url+"/admin/voting/question/add/")

        self.cleaner.find_element(By.NAME, "_save").click()

        self.assertTrue(self.cleaner.find_element_by_xpath('/html/body/div/div[3]/div/div[1]/div/form/div/p').text == 'Please correct the errors below.')
        self.assertTrue(self.cleaner.current_url == self.live_server_url+"/admin/voting/question/add/")

class VotingModelTestCase(BaseTestCase):
    def setUp(self):
        q = Question(desc='Descripcion')
        q.save()
        
        opt1 = QuestionOption(question=q, option='opcion 1')
        opt1.save()
        opt1 = QuestionOption(question=q, option='opcion 2')
        opt1.save()

        self.v = Voting(name='Votacion', question=q)
        self.v.save()
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.v = None

    def testExist(self):
        v=Voting.objects.get(name='Votacion')
        self.assertEquals(v.question.options.all()[0].option, "opcion 1")