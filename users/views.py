from django.views.generic.list import ListView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404

from .models import User


@method_decorator(login_required, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'

    def get_queryset(self):
        queryset = super().get_queryset().exclude(id=self.request.user.id)
        self.friends = self.request.GET.get('friends')

        if self.friends:
            return queryset.filter(friends=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friends'] = self.friends
        return context


@method_decorator(login_required, name='dispatch')
class FriendView(View):
    def get(self, request, user_id=None):
        if user_id == request.user.id:
            raise Http404()

        user = get_object_or_404(User, id=user_id)

        if user in request.user.friends.all():
            request.user.friends.remove(user)
        else:
            request.user.friends.add(user)

        return redirect(request.META.get('HTTP_REFERER'))
