from django.contrib.auth import login
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView

from core.forms import RegistrationForm


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


class ProductsNewView(TemplateView):
    template_name = 'products_new.html'


class ProductsEditView(TemplateView):
    template_name = 'products_edit.html'


class PurchasesListView(TemplateView):
    template_name = 'purchases_list.html'


class RefundsListView(TemplateView):
    template_name = 'refunds_list.html'
