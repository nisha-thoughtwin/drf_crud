"""drf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from employee.auth import CustomAuthToken
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import url
from django.utils.translation import gettext_lazy as _



def trigger_error(request):
    division_by_zero = 1 / 0


# urlpatterns = [
#     path('i18n/', include('django.conf.urls.i18n')),
#     path('', admin.site.urls),
#     path('employee/', include('employee.urls')),
#     path('gettoken/', obtain_auth_token),
#     path('custom_gettoken/', CustomAuthToken.as_view()),

#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
#     # path('verifytoken/', TokenVerifyView.as_view(), name='token_verify'),

#     path('sentry-debug/', trigger_error),


# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = i18n_patterns(
    path('', admin.site.urls),
    path('employee/', include('employee.urls')),
    path('gettoken/', obtain_auth_token),
    path('custom_gettoken/', CustomAuthToken.as_view()),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('verifytoken/', TokenVerifyView.as_view(), name='token_verify'),

    path('sentry-debug/', trigger_error),
        prefix_default_language=False
    )   + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)