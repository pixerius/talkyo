from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.BotListView.as_view(), name='list'),
]
