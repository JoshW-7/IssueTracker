from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers, serializers, viewsets

from .views import IssueViewSet, TagViewSet, StatusViewSet, ProjectViewSet


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'issues', IssueViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'tags', TagViewSet)
router.register(r'statuses', StatusViewSet)

vue_urls = [
    path('', lambda request: HttpResponse(render(request, 'vue_index.html'))),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('', include("issue.urls")),
]


