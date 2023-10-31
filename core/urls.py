from django.urls import path

from core.views import (
    HomeView,
    RegistrationView,
    LoginUserView,
    LogoutUserView,
    ProductListView,
    ProductAddView,
    ProductEditView,
    PurchaseListView,
    RefundsListView
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('products', ProductListView.as_view(), name='products'),
    path('products/new', ProductAddView.as_view(), name='product_add'),
    path('products/<int:pk>/edit/', ProductEditView.as_view(), name='product_edit'),
    path('purchases/', PurchaseListView.as_view(), name='purchases'),
    path('refunds/', RefundsListView.as_view(), name='refunds'),
]
