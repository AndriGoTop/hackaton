from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
<<<<<<< HEAD:hackaton/hackaton/apphub/urls.py
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
=======
    path("logout", views.logout_view, name="logout"),
    path('news/<int:pk>/', views.NewsDetailView, name='news_detail'),
>>>>>>> on_develop:hackaton/apphub/urls.py
]
