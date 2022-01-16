from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from datetime import datetime
from rest_framework import filters, generics, viewsets, permissions, status
from .models import Post
from rest_framework.views import APIView
from .permissions import IsAuthorOrReadOnly, IsAssigned
from .serializers import PostSerializer, UserSerializer


from rest_framework.renderers import HTMLFormRenderer, JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response


def test_cookie(request):
    if request.COOKIES.get('visits'):
        value = int(request.COOKIES.get('visits')) + 1
        response = HttpResponse(f"Witaj ponownie! Po raz {value}")
        response.set_cookie('visits', value)
        return response
    else:
        value = 1
        response = HttpResponse("Witaj po raz pierwszy.")
        response.set_cookie('visits', value)
        return response


class PostList(APIView):
    serializer_class = PostSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserList(generics.ListCreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsAuthorOrReadOnly)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsAuthorOrReadOnly)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username']

