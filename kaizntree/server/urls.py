from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.UserInfoAPIView.as_view(), name="log_in"),
    path("signup/", views.UserRegisterAPIView.as_view(), name="sign_up"),
    path("category/", views.UserCategoryAPIView.as_view(), name="category"),
    path("item/", views.UserItemsAPIView.as_view(), name="items"),
]