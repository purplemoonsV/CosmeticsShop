from os import name
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import re_path
from .views import *

urlpatterns = [
    path('', index,name="Index"),

    path('login', login,name="Login"),
    path('admin/login', loginAdmin,name="Admin"),
    path('logout', logout, name="logout"),
    path('logoutA', logoutA, name="logoutA"),
    path('register',register,name="Register"),

    path('shop',shop,name="Shop"),
    path('Shopcate/<int:id>',ShopCate,name="ShopCate"),

    path('Cart',Cart,name="Carts"),
    path('AddToCart',addCart,name="AddCarts"),
    path('CheckOut',Checkout,name="Checkout"),
    path('DeleteItem/<int:id>',DeleteItem,name="deleteitem"),
    # path('AddUpdateItem/<int:id>',AddUpdateItem,name="AddUpdateItem"),
    # path('RemoveUpdateItem/<int:id>',RemoveUpdateItem,name="RemoveUpdateItem"),
    path('product/<int:pk>/add',add_product,name='add_product'),
     path('product/<int:pk>/remove',remove_product,name='remove_product'),


    # path('AddFavourite/<int:id>',AddFavourite,name="AddFavourites"),
    path('FavouriteList',FavouriteList,name="FavouriteLists"),

    path('admin/product/',ProductManagement,name='pro_management'),
    path('product/detail/<int:id>',pro_detaill,name="pro_detaill"),

    path('admin/dashborad',dashborad,name="Dashborad"),
    path('admin/member',MemberManagement,name="mem_management"),

    path('admin/order',Orders,name="order_management"),
    path('admin/order/delete/<int:id>',OrderDelete,name="order_delete"),
    path('admin/order/ordertail/<int:id>',OrderDetails,name="order_detail"),

    path('admin/category',Categorys,name="cate_management"),
    path('admin/category/create',CategorysCreate,name="cate_create"),
    path('admin/category/update/<int:id>',CategoryUpdate,name="cate_update"),
    path('admin/category/delete/<int:id>',CategorysDelete,name="cate_delete"),

    path('admin/payment',Payments,name="payment_management"),
    path('payment/create',PaymentCreate,name="payment_create"),
    path('admin/payment/confirm/<int:id>',Confirm,name="payment_confirm"),

    path('review/<int:id>',Review,name="Addreview"),

    path('admin/category/update/<int:id>',CategoryUpdate,name="cate_update"),
    path('admin/category/delete/<int:id>',CategorysDelete,name="cate_delete"),

    path('admin/size',Sizes,name="size_management"),
    path('admin/size/create',SizeCreate,name="size_create"),
    path('admin/size/update/<int:id>',SizeUpdate,name="size_update"),
    path('admin/size/delete/<int:id>',SizeDelete,name="size_delete"),

    path('pdf/',report_order,name="ReportOrder"),
    path('pdf/order/<int:id>',report_orderdetail,name="ReportOrderDetail"),

    path('member/update/<int:id>',MemberUpdate,name='mem_update'),
    path('member/delete/<int:id>/',MemberDelete,name='mem_delete'),

    path('product/create', ProductCreate, name='pro_create'),
    path('product/update/<int:id>/',ProductUpdate, name='pro_update'),
    path('product/delete/<int:id>/',ProductDelete, name='pro_delete'),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)