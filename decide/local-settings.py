ALLOWED_HOSTS = ["decidepicasso.pythonanywhere.com"]

Modules in use, commented modules that you won't use
MODULES = [
    'authentication',
    'base',
    'booth',
    'census',
    'mixnet',
    'postproc',
    'store',
    'visualizer',
    'voting',
]

BASEURL = 'http://localhost:8000/'

APIS = {
    'authentication': BASEURL,
    'base': BASEURL,
    'booth': BASEURL,
    'census': BASEURL,
    'mixnet': BASEURL,
    'postproc': BASEURL,
    'store': BASEURL,
    'visualizer': BASEURL,
    'voting': BASEURL,
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'decidepicasso$default',
        'USER': 'decidepicasso',
        'PASSWORD':'databaseegc',
        'HOST': 'decidepicasso.mysql.pythonanywhere-services.com',
        'CHARSET': 'uft8',
    }
}

KEYBITS = 256
