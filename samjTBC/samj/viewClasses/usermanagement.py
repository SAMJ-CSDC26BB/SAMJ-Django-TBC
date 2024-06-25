from django.shortcuts import redirect
from django.views.generic import TemplateView
from allauth.account.forms import UserForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from ..models import User

class UserManagementView(LoginRequiredMixin, TemplateView):
    template_name = "user_management.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['user_form'] = UserForm()
        context['status_options'] = [choice for choice in User.STATUS_CHOICES if choice[0] != 'deleted']
        context['role_options'] = User.ROLE_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_management')
        context = self.get_context_data()
        context['user_form'] = form
        return self.render_to_response(context)