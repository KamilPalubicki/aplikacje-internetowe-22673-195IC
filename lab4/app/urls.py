from django.urls import path
from .views import PostList, PostDetail, PostViewSet
from .views import UserList, UserDetail, UserViewSet
from rest_framework.routers import SimpleRouter
from . import views


urlpatterns = [
     path('<int:pk>/', PostDetail.as_view()),
     path('', PostList.as_view()),
     path('test_cookie/', views.test_cookie, name='test_cookie'),
     path('users/', UserList.as_view()),
     path('users/<int:pk>/', UserDetail.as_view()),
]

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')
router.register('', PostViewSet, basename='post')
urlpatterns = router.urls
