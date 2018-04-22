from django.conf.urls import url
from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from quickstart import views

urlpatterns = [
    url(r'^quickstart/$', views.curr_list),
    url(r'^quickstart/update_rates/$', views.update_rates),
    path('quickstart/<str:fromto>/<int:amount>/', views.convert),


]

urlpatterns = format_suffix_patterns(urlpatterns)