from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.listing, name="specialization-listing"),
    url(r'^list$', views.lists, name="specialization-lists"),
    url(r'^add$', views.add, name="add"),
    url(r'^delete/(?P<id>\w{0,50})/$', views.delete, name="delete"),
    url(r'^update/(?P<specializationId>\w{0,50})/$', views.update, name="update"),
]
