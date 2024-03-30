from django.urls import path, include
from .views import (
    RegisterView,
    LoginView,
    UserViewSet,
    RefreshAPIView,
    LogoutAPIView,
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("register", RegisterView.as_view()),
    path("login", LoginView.as_view()),
    path("", include(router.urls)),
    path("refresh", RefreshAPIView.as_view()),
    path("logout", LogoutAPIView.as_view()),
]
