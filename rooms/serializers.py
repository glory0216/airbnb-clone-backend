from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Amenity, Room
from common.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
# from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


class AmenitySerializer(ModelSerializer):

    class Meta:
        model = Amenity
        fields = (
            "name",
            "description"
        )


class RoomListSerializer(ModelSerializer):

    rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            "id",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user


class RoomDetailSerializer(ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    ## reviews = ReviewSerializer(many=True, read_only=True) ## 역접근자를 사용하면, one to many일 경우, 모든 data를 조회하기 때문에 사용하면 안됨, URL을 분리할 것
    is_liked = SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user

    def get_is_liked(self, room):
        request = self.context["request"]
        return Wishlist.objects.filter(user=request.user, rooms__pk=room.pk).exists()


class HostRoomSerializer(ModelSerializer):

    rating = SerializerMethodField()
    total_reviews = SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "kind",
            "rating",
            "total_reviews",
        )

    def get_rating(self, room):
        return room.rating()

    def get_total_reviews(self, room):
        return room.total_reviews()
