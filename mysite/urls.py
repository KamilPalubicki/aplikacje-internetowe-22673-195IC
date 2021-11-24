from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path(
            'change_password/',
            auth_views.PasswordChangeView.as_view(template_name='registration/change_password.html'),
        ),
    path(
             'login/',
             auth_views.PasswordChangeView.as_view(template_name='registration/login.html'),
        ),
    path(
             'signup/',
             auth_views.PasswordChangeView.as_view(template_name='registration/signup.html'),
         ),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]