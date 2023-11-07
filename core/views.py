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


class ProductAddView(SuperuserRequiredMixin, CreateView):
    template_name = 'product_add.html'
    model = Product
    fields = ['name', 'description', 'price', 'quantity']
    success_url = reverse_lazy('core:products')


class ProductPurchaseView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    form_class = PurchaseForm
    success_url = reverse_lazy('core:products')

    def form_valid(self, form):
        product_pk = self.request.POST.get('product_pk')
        product = Product.objects.get(id=product_pk)
        quantity = int(self.request.POST.get('quantity'))
        user = self.request.user
        page_number = self.request.GET.get('page')

        flag = True
        if product.price * quantity > user.wallet:
            messages.error(self.request, "Not enough cash")
            flag = False

        if product.quantity < quantity:
            messages.error(self.request, "Not enough products")
            flag = False

        if flag:
            purchase = Purchase(quantity=quantity, user=user, product=product)
            purchase.save()

            product.quantity -= quantity
            product.save()

            user.wallet -= product.price * quantity
            user.save()

            messages.success(self.request, 'Successful purchase')

        return HttpResponseRedirect(f"{self.success_url}?page={page_number}")

    def form_invalid(self, form):
        quantity = int(self.request.POST.get('quantity'))
        page_number = self.request.GET.get('page')

        if not quantity:
            messages.warning(self.request, "You need to select the quantity of the product")

        return HttpResponseRedirect(f"{self.success_url}?page={page_number}")


class ProductListView(ListView):
    template_name = 'product_list.html'
    model = Product
    ordering = ['price']
    paginate_by = 3


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
