from django.urls import path
from . import views
app_name = 'cart'
urlpatterns = [
    # path('<int:id>', views.cart_homee, name='cart_homee'),
    path('', views.cart_home, name='cart_home'),
    path('add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('update/<int:id>/', views.update_qty, name='update_qty'),
    path('remove/<int:id>/', views.remove_item, name='remove_item'),
    path('address/', views.address_page, name='address_page'),
    path('address/<int:item_id>/', views.address_page, name='address_page_single'),
    path('payment/', views.payment_page, name='payment_page'),
    path('payment/<int:item_id>/', views.payment_page, name='payment_page_single'),
    path('success/', views.order_success, name='order_success'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:id>/', views.order_detail, name='order_detail'),
]


