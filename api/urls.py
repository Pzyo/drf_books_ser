
from django.urls import path, re_path
from api import views

urlpatterns = [
    path(r'books/', views.BookAPIView.as_view()),
    path(r'books2/', views.BookView.as_view()),
    re_path(r'^books/(?P<pk>\d+)$', views.BookAPIView.as_view()),
]