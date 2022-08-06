from rest_framework.routers import DefaultRouter
from django.urls import path

from user.views import UserViewset, LoginView

router = DefaultRouter(trailing_slash=False)
router.register('users', UserViewset, 'users')

urlpatterns = router.urls
urlpatterns += [
    path('login', LoginView.as_view(), name='login'),
]