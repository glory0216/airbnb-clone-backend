from django.db.models import Avg, Count
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from reviews.models import Review
from reviews.serializers import UserReviewSerializer, HostReviewSerializer
from rooms.models import Room
from rooms.serializers import HostRoomSerializer
from .models import User


class PrivateUserSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = (
            "id",
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )


class PublicUserSerializer(ModelSerializer):

    reviews = SerializerMethodField()
    rooms = SerializerMethodField()
    host_reviews = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "avatar",
            "name",
            "last_login",
            "date_joined",
            "reviews",
            "is_host",
            "rooms",
            "host_reviews",
            "gender",
            "language",
            "currency",
        )

    def get_reviews(self, user):
        recent_reviews = Review.objects.filter(user=user).order_by("-created_at")[:10]
        serializer = UserReviewSerializer(recent_reviews, many=True)
        return serializer.data

    def get_rooms(self, owner):
        query_exp = {
            "cnt_reviews": Count("reviews"),
            "avg_ratings": Avg("reviews__rating"),
        }
        ordering = ["-cnt_reviews", "-avg_ratings"]
        owned_rooms = Room.objects.filter(owner=owner).annotate(**query_exp).order_by(*ordering)[:10]
        serializer = HostRoomSerializer(owned_rooms, many=True)
        return serializer.data

    def get_host_reviews(self, owner):
        reviews = Review.objects.filter(room__owner=owner)[:10]
        serializer = HostReviewSerializer(reviews, many=True)
        return serializer.data
