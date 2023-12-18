import json

from random import choice
from random import randint

from locust import (
    HttpUser,
    SequentialTaskSet,
    TaskSet,
    task,
    between
)


HOST = "http://localhost:8080"
VOTING = 2


class DefVisualizer(TaskSet):

    @task
    def index(self):
        self.client.get("/visualizer/{0}/".format(VOTING))


class DefVoters(SequentialTaskSet):

    def on_start(self):
        with open('voters.json') as f:
            self.voters = json.loads(f.read())
        self.voter = choice(list(self.voters.items()))

    @task
    def login(self):
        username, pwd = self.voter
        self.token = self.client.post("/authentication/login/", {
            "username": username,
            "password": pwd,
        }).json()

    @task
    def getuser(self):
        self.usr= self.client.post("/authentication/getuser/", self.token).json()
        print( str(self.user))

    @task
    def voting(self):
        headers = {
            'Authorization': 'Token ' + self.token.get('token'),
            'content-type': 'application/json'
        }
        self.client.post("/store/", json.dumps({
            "token": self.token.get('token'),
            "vote": {
                "a": "12",
                "b": "64"
            },
            "voter": self.usr.get('id'),
            "voting": VOTING
        }), headers=headers)


    def on_quit(self):
        self.voter = None

class Visualizer(HttpUser):
    host = HOST
    tasks = [DefVisualizer]
    wait_time = between(3,5)



class Voters(HttpUser):
    host = HOST
    tasks = [DefVoters]
    wait_time= between(3,5)


class UserBehavior(HttpUser):
    wait_time = between(5, 9)
    
    def load_user_data(self):
        with open('register.json') as file:
            return json.load(file)

    @task
    def signup(self):
        user_data = self.load_user_data()

        # Selecciona un usuario aleatorio del JSON
        user = choice(list(user_data.values()))

        # Obtiene el token CSRF de una solicitud GET a la página de registro
        response = self.client.get("/signup/") 

        # Extrae el token CSRF de la cookie
        csrf_token = response.cookies.get('csrftoken', '')

        # Envia los datos al endpoint /signup/ incluyendo el token CSRF
        headers = {'X-CSRFToken': csrf_token}

        # Envia los datos al endpoint /signup/ utilizando el formato request.POST
        response = self.client.post("/signup/", data={
            'username': user['username'],
            'password1': user['password1'],
            'password2': user['password2'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'email': user['email']
        }, headers = headers)

        if response.status_code == 302:  # Revisa si se redirige a la página de inicio de sesión
            print(f"User {user['username']} created successfully")
        else:
            print(f"Failed to create user {user['username']}: {response.status_code}")
            print(response.text)
