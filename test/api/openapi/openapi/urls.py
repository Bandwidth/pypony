from django.urls import path, include, re_path
from rest_framework import routers

from users.views import UserViewSet
from . import views

router = routers.SimpleRouter(trailing_slash=False)

# Register models here
router.register('users', UserViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'/?', include(router.urls)),
]
