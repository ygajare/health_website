from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.listing, name="dspecialization-listing"),
    url(r'^doctor/(?P<userId>\w{0,50})/$', views.doctor_specialization, name="doctor_specialization"),
    url(r'^add$', views.add, name="add"),
    url(r'^delete/(?P<id>\w{0,50})/$', views.delete, name="delete"),
    url(r'^update/(?P<dspecializationId>\w{0,50})/$', views.update, name="update"),
]
