"""challenge2 URL Configuration

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
from django.contrib.auth.models import User
from api_stuff.models import FileUpload
from django.urls import path, include
from rest_framework import routers, serializers, viewsets
#from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework import mixins
from django.shortcuts import redirect
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#from django.views.generic import TemplateView

class CreateListRetrieveViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    pass

# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'is_staff']

# class UserViewSet(CreateListRetrieveViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class FileSerializer(serializers.HyperlinkedModelSerializer):
#     #file = serializers.FileField()
#     class Meta:
#         model = FileUpload
#         fields = ['file']

# class FileViewSet(CreateListRetrieveViewSet):
#     queryset = FileUpload.objects.all()
#     serializer_class = FileSerializer

from api_stuff.views import FileViewSet, SaveXmlViewSet, ApiViewSet, FeaturesViewSet, WeatherViewSet, InfoViewSet



router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)
router.register(r'info', InfoViewSet, basename='info')
router.register(r'weather', WeatherViewSet, basename='weather')
router.register(r'features', FeaturesViewSet, basename='features')
router.register(r'api', ApiViewSet, basename='api')
router.register(r'files', FileViewSet, basename='files')
router.register(r'save_xml', SaveXmlViewSet, basename='save_xml')

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', lambda req: redirect('docs/')),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('schema/', get_schema_view(
    #     title='get schema view',
    #     description='API for the stuff',
    #     version="1.0.0"
    # ), name='openapi-schema'),
    path('docs/', include_docs_urls(title="API v0.0.1"))
]

urlpatterns += router.urls
urlpatterns += staticfiles_urlpatterns()