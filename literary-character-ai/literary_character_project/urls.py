# literary_character_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from characters.views import landing_page, signup, CustomLogoutView
from characters.forms import EmailLoginForm

urlpatterns = [
    path('admin/', admin.site.urls),

    # App-specific URLs (list, detail, history, API) under '/app/' prefix
    path('app/', include('characters.urls')),

    # Site-wide pages
    path('', landing_page, name='landing_page'),

    # Authentication URLs
    path('accounts/signup/', signup, name='signup'), # Custom signup view
    path('accounts/login/', auth_views.LoginView.as_view(
            template_name='registration/login.html',
            authentication_form=EmailLoginForm # Using a custom email login form
        ), name='login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'), # Custom logout view

    # Include default Django auth URLs (for password reset, change, etc.)
    # This comes *after* custom login/logout to avoid overriding them.
    path('accounts/', include('django.contrib.auth.urls')),

]

# Serve media files uploaded by users during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


