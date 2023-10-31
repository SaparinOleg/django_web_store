from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView, UpdateView, CreateView
from django.urls import reverse, reverse_lazy

from core.forms import RegistrationForm, PurchaseForm
from core.models import Product, Purchase, User


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
        return reverse_lazy('core:home')


class LogoutUserView(LogoutView):
    template_name = 'registration/logout.html'

    def get_success_url(self):
        return reverse_lazy('core:home')


class ProductListView(ListView):
    template_name = 'product_list.html'
    model = Product
    ordering = ['price']
    paginate_by = 3


class ProductAddView(SuperuserRequiredMixin, CreateView):
    template_name = 'product_add.html'
    model = Product
    fields = ['name', 'description', 'price', 'quantity']
    success_url = reverse_lazy('core:products')


class ProductEditView(SuperuserRequiredMixin, UpdateView):
    template_name = 'product_edit.html'
    model = Product
    login_url = 'core:products'
    fields = ['name', 'description', 'price', 'quantity']

    def get_success_url(self):
        return reverse_lazy('core:products')


class PurchaseListView(LoginRequiredMixin, TemplateView):
    template_name = 'purchase_list.html'
    login_url = 'core:login'


class RefundsListView(SuperuserRequiredMixin, TemplateView):
    template_name = 'refund_list.html'
