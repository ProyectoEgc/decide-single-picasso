from django.urls import path
from .views import VisualizerView
from  postproc import views


urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
]
