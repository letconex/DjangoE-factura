from django.urls import path
from . import views

urlpatterns = [
        path("", views.crmindex, name="crmindex"),
        path("login", views.login_user, name="login"),
        path("logout", views.logout_user, name="logout"),
        # path("", views.crmindex, name="crmindex"),
]