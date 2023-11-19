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
    RefundsListView,
    ProductPurchaseView,
    PurchaseRefundView,
    RefundsAcceptView,
    RefundsDeclineView,
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/new/', ProductAddView.as_view(), name='product_add'),
    path('products/<int:pk>/edit/', ProductEditView.as_view(), name='product_edit'),
    path('products/purchase/', ProductPurchaseView.as_view(), name='product_purchase'),
    path('purchases/', PurchaseListView.as_view(), name='purchases'),
    path('purchases/refund', PurchaseRefundView.as_view(), name='purchase_refund'),
    path('refunds/', RefundsListView.as_view(), name='refunds'),
    path('refunds/accept/<int:pk>', RefundsAcceptView.as_view(), name='refunds_accept'),
    path('refunds/decline/<int:pk>', RefundsDeclineView.as_view(), name='refunds_decline'),
]
