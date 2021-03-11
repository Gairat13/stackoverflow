"""stack_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view

from main.views import *

router = DefaultRouter()
router.register('problems', ProblemViewSet)
router.register('replies', ReplyViewSet)
router.register('comments', CommentViewSet)

schema_view = get_schema_view(
    openapi.Info(
          title="Snippets API",
          default_version='v1',
          description="Test description",
          terms_of_service="https://www.google.com/policies/terms/",
          contact=openapi.Contact(email="contact@snippets.local"),
          license=openapi.License(name="BSD License"),
       ),
    public=True,
)

urlpatterns = [
    path('api/v1/docs/', schema_view.with_ui()),
    path('admin/', admin.site.urls),
    # path('api/v1/', include('main.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/accounts/', include('account.urls'))
]

