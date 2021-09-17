from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.listing, name="quotation-listing"),
    url(r'^list$', views.lists, name="quotation-lists"),
    url(r'^add/(?P<specializationId>\w{0,50})/$', views.add, name="add"),
    url(r'^details/(?P<quotationId>\w{0,50})/$', views.details, name="details"),
    url(r'^reply-details/(?P<replyId>\w{0,50})/$', views.reply_details, name="reply_details"),
    url(r'^finalize/(?P<replyId>\w{0,50})/(?P<quotationId>\w{0,50})/$', views.finalize, name="finalize"),
    url(r'^reply/(?P<quotationId>\w{0,50})/$', views.quotation_reply, name="quotation_reply"),
    url(r'^delete/(?P<id>\w{0,50})/$', views.delete, name="delete"),
    url(r'^update/(?P<quotationId>\w{0,50})/$', views.update, name="update"),
]
