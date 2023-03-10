from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from reviews.models import Review
from reviews.serializers import UserReviewSerializer, HostReviewSerializer
from rooms.models import Room
from rooms.serializers import HostRoomSerializer
from . import serializers
from .models import User


class Me(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):

    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError

        serializer = serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()

            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublicUser(APIView):

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        # serializer = serializers.PrivateUserSerializer(user) ## public user serailizer 작성해보기
        serializer = serializers.PublicUserSerializer(user)
        return Response(serializer.data)


class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError


class Login(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"ok": "Welcome"})
        else:
            return Response({"error": "wrong password"})


class Logout(APIView):

    def post(self, request):
        logout(request)
        return Response({"ok": "Bye"})


class UserReviews(APIView):

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, username):
        user = self.get_object(username)
        reviews = Review.objects.filter(user=user)\
            .order_by("-created_at")
        serializer = UserReviewSerializer(
            reviews,
            many=True,
        )
        return Response(serializer.data)


class HostRooms(APIView):

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, username):
        owner = self.get_object(username)
        if not owner.is_host:
            raise ParseError("Not a host")
        rooms = Room.objects.filter(owner=owner).order_by("-created_at")
        serializer = HostRoomSerializer(
            rooms,
            many=True
        )
        return Response(serializer.data)


class HostReviews(APIView):

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, username):
        owner = self.get_object(username)
        if not owner.is_host:
            raise ParseError("Not a host")
        reviews = Review.objects.filter(room__owner=owner).order_by("-created_at")
        serializer = HostReviewSerializer(
            reviews,
            many=True
        )
        return Response(serializer.data)
