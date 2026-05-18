from django.urls import path
from .import views
app_name = 'product'
urlpatterns=[
    path('',views.Index,name='index'),
    path('hoodie/',views.Hoodie,name="hoodie"),
    path('Five-sleeve/',views.Five_sleeve,name="five_sleeve"),
    path('regular/',views.Regular_fit,name='regular'),
    path('sleevless/',views.Sleevless,name='sleeve'),

    # path('',views.New_collection,name='neww')
    path('one/<int:id>',views.One_product,name='one_product'),
    path('onee/<int:id>',views.One_products,name='one_products'),

]