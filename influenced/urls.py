"""influenced URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from rest_framework import routers

from influencedapi.views.auth import check_user, register_user
from influencedapi.views.user_view import UserView
from influencedapi.views.job_view import JobView
from influencedapi.views.rating_view import RatingViewSet
from influencedapi.views.application_view import ApplicationViewSet
from influencedapi.views.socials_view import SocialsViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserView, 'user')
router.register(r'jobs', JobView, 'job')
router.register(r'ratings', RatingViewSet, 'rating')
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'socials', SocialsViewSet , basename='social')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('register', register_user),
    path('checkuser', check_user),
]
