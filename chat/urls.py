from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import ChatViewset

router = DefaultRouter(trailing_slash=False)
router.register('chats', ChatViewset, 'chats')

urlpatterns = router.urls
urlpatterns += []