from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
                # path(r'', views.index, name='index'),
                # path(r'about/', views.about, name='about'),
                # path('detail/<str:cat_no>/', views.detail, name='detail_view'),
                # path(r'lab6a/', views.new_index, name='new_index'),
                # path(r'lab6a/about', views.new_about, name='new_about'),
                # path('lab6a/detail/<str:cat_no>/', views.new_detail, name='new_detail'),
                path(r'', views.part2_index, name='part2_index'),
                path(r'about/', views.part2_about, name='part2_about'),
                path('detail/<str:cat_no>/', views.part2_detail, name='part2_detail'),
                path('products/', views.products, name='products'),
                path('place_order/', views.place_order, name='place_order'),
                path('products/<str:prod_id>', views.productdetail, name='productdetail'),
                path(r'login/', views.user_login, name='login'),
                path(r'register/', views.user_register, name='register'),
                path(r'logout/', views.user_logout, name='logout'),
                path(r'reset_password/', views.reset_password, name='reset_password'),
                path(r'myorders/', views.myorders, name='myorders'),
                path(r'myprofile/', views.myprofile, name='myprofile')
]
