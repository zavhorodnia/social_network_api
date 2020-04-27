from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    UserActivitySerializer, PostSerializer, LikeSerializer)
from .models import Post, NetworkUser, Like
from datetime import date, datetime


class UserSignup(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLogin(RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NetworkUsers(APIView):
    def get(self, request):
        users = NetworkUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostsByUser(APIView):
    def get(self, request, user_id):
        try:
            user = NetworkUser.objects.get(id=user_id)
        except NetworkUser.DoesNotExist:
            return Response('Wrong user id', status=status.HTTP_400_BAD_REQUEST)
        posts = user.posts
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class LikePost(APIView):
    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            post.likes.get(user_id=request.user.id)
        except Post.DoesNotExist:
            return Response("Wrong post id", status=status.HTTP_400_BAD_REQUEST)
        except Like.DoesNotExist:
            like = Like(user=request.user, post=post)
            like.save()
        serializer = PostSerializer(post)
        return Response(serializer.data)


class UnlikePost(APIView):
    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            like = post.likes.get(user_id=request.user.id)
            like.delete()
        except Post.DoesNotExist:
            return Response("Wrong post id", status=status.HTTP_400_BAD_REQUEST)
        except Like.DoesNotExist:
            pass
        serializer = PostSerializer(post)
        return Response(serializer.data)


class UserActivity(APIView):
    def get(self, request, user_id):
        try:
            user = NetworkUser.objects.get(id=user_id)
        except NetworkUser.DoesNotExist:
            return Response("Wrong user id", status=status.HTTP_400_BAD_REQUEST)
        serializer = UserActivitySerializer(user)
        return Response(serializer.data)


class Analytics(APIView):
    def get(self, request):
        try:
            date_str = request.GET.get('date_from', '1-1-1970')
            date_from = datetime.strptime(date_str, '%d-%m-%Y').date()
            date_str = request.GET.get('date_to', date.today().strftime('%d-%m-%Y'))
            date_to = datetime.strptime(date_str, '%d-%m-%Y').date()
        except ValueError:
            return Response('Invalid request format', status=status.HTTP_400_BAD_REQUEST)
        likes = Like.objects.filter(date__range=[date_from, date_to])
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)
