from django.contrib.auth import login
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy

from core.forms import RegistrationForm


class SuperuserRequiredMixin(UserPassesTestMixin, AccessMixin):
    login_url = 'core:home'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse(self.login_url))


class HomeView(TemplateView):
    template_name = 'home.html'


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.wallet = 10000
        user.save()
        login(self.request, user)
        return super().form_valid(form)


class LoginUserView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse('core:home')


class LogoutUserView(LogoutView):
    template_name = 'registration/logout.html'

    def get_success_url(self):
        return reverse('core:home')


class ProductsListView(TemplateView):
    template_name = 'products_list.html'


class ProductsNewView(SuperuserRequiredMixin, TemplateView):
    template_name = 'products_new.html'
    login_url = 'core:products'


class ProductsEditView(SuperuserRequiredMixin, TemplateView):
    template_name = 'products_edit.html'
    login_url = 'core:products'


class PurchasesListView(LoginRequiredMixin, TemplateView):
    template_name = 'purchases_list.html'
    login_url = 'core:login'


class RefundsListView(SuperuserRequiredMixin, TemplateView):
    template_name = 'refunds_list.html'
