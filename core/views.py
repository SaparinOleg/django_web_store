from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView, UpdateView, CreateView, DeleteView
from django.urls import reverse, reverse_lazy

from core.forms import RegistrationForm, PurchaseForm, RefundForm
from core.models import Product, Purchase, User, Refund


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


class PurchaseListView(LoginRequiredMixin, ListView):
    template_name = 'purchase_list.html'
    model = Purchase
    login_url = 'core:login'
    context_object_name = 'purchases'
    paginate_by = 10

    def get_queryset(self):
        ordering = self.request.GET.get('ordering', 'purchased_at')
        return Purchase.objects.filter(user=self.request.user)


class RefundsListView(SuperuserRequiredMixin, ListView):
    template_name = 'refund_list.html'
    model = Refund
    login_url = 'core:login'
    context_object_name = 'refunds'
    paginate_by = 3

    def get_queryset(self):
        return Refund.objects.get_queryset()


class PurchaseRefundView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    form_class = RefundForm
    success_url = reverse_lazy('core:purchases')

    def form_valid(self, form):
        purchase_pk = self.request.POST.get('purchase_pk')
        purchase = Purchase.objects.get(id=purchase_pk)

        if len(Refund.objects.filter(purchase=purchase)):
            messages.error(self.request, "Refund already created")
        elif timezone.now() - purchase.purchased_at > timedelta(minutes=3):
            messages.error(self.request, "Time's up! You had a total of 3 minutes for the refund")
        else:
            refund = form.save(commit=False)
            refund.purchase = purchase
            refund.save()
            messages.success(self.request, "Your refund has been successfully initiated and is currently under review")
        return HttpResponseRedirect(self.success_url)


class RefundsAcceptView(SuperuserRequiredMixin, CreateView):
    login_url = 'login'
    model = Refund
    success_url = reverse_lazy('core:refunds')

    def post(self, request, *args, **kwargs):
        refund = self.get_object()
        purchase = refund.purchase
        product = purchase.product
        user = purchase.user

        product.quantity += purchase.quantity
        product.save()
        user.wallet += purchase.product.price * purchase.quantity
        user.save()

        purchase.delete()
        refund.delete()
        return HttpResponseRedirect(self.success_url)


class RefundsDeclineView(SuperuserRequiredMixin, DeleteView):
    login_url = 'login'
    model = Refund
    success_url = reverse_lazy('core:refunds')

    def post(self, request, *args, **kwargs):
        refund = self.get_object()
        refund.delete()
        return HttpResponseRedirect(self.success_url)
