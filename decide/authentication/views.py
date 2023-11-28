from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.status import (
        HTTP_201_CREATED,
        HTTP_400_BAD_REQUEST,
        HTTP_401_UNAUTHORIZED
)
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from .serializers import UserSerializer
from django.template import loader
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth import logout

from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from census.models import Census
from voting.models import Voting
from django.urls import resolve, Resolver404
from django.utils import translation
from decide.settings import LANGUAGES


def home(request):
    return render(request,'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')

    elif request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                # Utiliza los campos del formulario personalizado
                user = User.objects.create_user(
                    username=username,
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    email=request.POST['email'],
                    password=password1
                )
                user.save()
                return HttpResponse('User created successfully')
            except Exception as e:
                return HttpResponse(f'Error creating user: {str(e)}')

        return HttpResponse('Passwords do not match')

    return HttpResponse('Invalid request method')

class GetUserView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        return Response(UserSerializer(tk.user, many=False).data)


class LogoutView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        try:
            tk = Token.objects.get(key=key)
            tk.delete()
        except ObjectDoesNotExist:
            pass

        return Response({})


class RegisterView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        if not tk.user.is_superuser:
            return Response({}, status=HTTP_401_UNAUTHORIZED)

        username = request.data.get('username', '')
        pwd = request.data.get('password', '')
        if not username or not pwd:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        try:
            user = User(username=username)
            user.set_password(pwd)
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
        except IntegrityError:
            return Response({}, status=HTTP_400_BAD_REQUEST)
        return Response({'user_pk': user.pk, 'token': token.key}, HTTP_201_CREATED)

def home(request):
    if(request.user.is_authenticated == True):
        template = loader.get_template("authentication/decide.html")
    else:
        return redirect('/authentication/login-view')
    context = {}
    votings=[]
    closed_votings=[]
    if request.user.is_authenticated == True:
        authenticated = True
        context['username'] = request.user.username
        census = Census.objects.filter(voter_id=request.user.id)
        for c in census:
            voting_id = c.voting_id

            voting = Voting.objects.get(id = voting_id)
            
            if voting is not None and voting.start_date is not None and voting.end_date is None:
                votings.append(voting) 
            if voting is not None and voting.start_date is not None and voting.end_date is not None:
                closed_votings.append(voting)

    context['authenticated'] = authenticated
    context['votings'] = votings
    context['closed_votings'] = closed_votings

    return HttpResponse(template.render(context, request))

class LoginView(View):

    template_name = "authentication/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password1')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            # Handle invalid login credentials here
            return render(request, self.template_name, {'error_message': 'Invalid login credentials'})


    @staticmethod     
    def authenticated(request):
        return render(request, 'authentication/authenticated.html', {
                'username' : request.user
            })
    
def logout_view(request):
    response = redirect("/")
    if request.user.is_authenticated == True:
        logout(request)
        response.delete_cookie('token')
        response.delete_cookie('decide')
    return response

def is_safe_url(url):
    try:
        resolve(url)
        return True
    except Resolver404:
        return False

def change_language(request, language_code):
    allowed_languages = [lang[0] for lang in translation.settings.LANGUAGES]

    if language_code in allowed_languages:
        request.session[translation.LANGUAGE_SESSION_KEY] = language_code
        return redirect('/')

    return redirect('/')

