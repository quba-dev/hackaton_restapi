from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegistrationAPIView.as_view()),
    path('activate/<str:activation_code>', views.ActivationView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
]