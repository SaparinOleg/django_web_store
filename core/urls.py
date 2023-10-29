from django.urls import path

from core.views import (
    HomeView,
    RegistrationView,
    LoginUserView,
    LogoutUserView,
    ProductsListView,
    ProductsNewView,
    ProductsEditView,
    PurchasesListView,
    RefundsListView
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('products', ProductsListView.as_view(), name='products'),
    path('products/new', ProductsNewView.as_view(), name='products_new'),
    path('products/edit', ProductsEditView.as_view(), name='products_edit'),
    path('purchases', PurchasesListView.as_view(), name='purchases'),
    path('refunds', RefundsListView.as_view(), name='refunds'),
]
