from django.urls import path

from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.redirect_login, name="redirect-login"),
    path('login', views.login_view, name="login"),
    path('dashboard', views.dashboard, name="main"),
    path('check', views.login_create, name="check"),
    path('logout', views.logout_view, name="logout"),
    path('register/bling', views.register_bling_user, name="bling_register"),
    path('bling/data', views.get_data, name="bling_data")
]
