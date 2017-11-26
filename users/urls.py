from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [

    url(r'^login/$',
        auth_views.LoginView.as_view(),
        name='login'),

    url(r'^logout/$',
        auth_views.LogoutView.as_view(),
        name='logout'),

    url(r'^friend/(?P<user_id>\d+)/$',
        views.FriendView.as_view(),
        name='friend'),

    url(r'^friends/$',
        views.UserListView.as_view(),
        name='list'),

]
