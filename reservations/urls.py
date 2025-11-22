from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('details/', views.details, name='details'),
    path('checkout/', views.checkout, name='checkout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('api/chat/', views.chat_view, name='chat_api'),
]
