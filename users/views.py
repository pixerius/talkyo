from django.views.generic.list import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404

from .models import User


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'

    def get_queryset(self):
        queryset = super().get_queryset().exclude(id=self.request.user.id)
        query = self.request.GET.get('query')

        if query:
            return queryset.filter(name__icontains=query)

        return queryset.filter(friends=self.request.user)


class FriendView(LoginRequiredMixin, View):
    def get(self, request, user_id=None):
        if user_id == request.user.id:
            raise Http404()

        user = get_object_or_404(User, id=user_id)

        if user in request.user.friends.all():
            request.user.friends.remove(user)
        else:
            request.user.friends.add(user)

        return redirect(request.META.get('HTTP_REFERER'))
