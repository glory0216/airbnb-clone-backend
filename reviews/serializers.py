from rest_framework import serializers
from common.serializers import TinyUserSerializer, TinyRoomSerializer
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):

    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            "user",
            "payload",
            "rating",
        )


class UserReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = (
            "payload",
            "rating",
            "created_at",
        )


class HostReviewSerializer(serializers.ModelSerializer):

    user = TinyUserSerializer(read_only=True)
    room = TinyRoomSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            "user",
            "room",
            "payload",
            "rating",
            "created_at"
        )
