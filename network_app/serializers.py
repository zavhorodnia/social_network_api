from rest_framework_simplejwt.serializers import TokenObtainSlidingSerializer
from rest_framework import serializers
from .models import Post, NetworkUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'text', 'author', 'published', 'likes_count']

    def get_likes_count(self, obj):
        return obj.liked_by.count()


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkUser
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserRegistrationSerializer, self).create(validated_data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=25)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'Wrong username or password, login failed')
        try:
            jwt_token = TokenObtainSlidingSerializer.get_token(user)
            update_last_login(None, user)
        except NetworkUser.DoesNotExist:
            raise serializers.ValidationError(
                'User with the given credentials does not exist')
        return {
            'username': user.username,
            'token': jwt_token
        }


class UserSerializer(serializers.ModelSerializer):
    # liked_posts = PostSerializer(many=True, read_only=True)
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = NetworkUser
        fields = ['id', 'username', 'posts'] # , 'liked_posts']
        # extra_kwargs = {'liked_posts': {'required': False}}


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkUser
        fields = ['last_login', 'last_request']
