from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class CreateRoomBookingSerializer(serializers.ModelSerializer):

    ## required로 만들기위해 선언
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests"
        )

    def validate_check_in(self, value): ## validate_컬럼명으로 is_valid 에서 valid할 요소를 overwrite 할 수 있음
        today = timezone.localtime(timezone.now()).date()
        if today > value:
            raise serializers.ValidationError("Can't book in the past.")

        return value

    def validate_check_out(self, value): ## validate_컬럼명으로 is_valid 에서 valid할 요소를 overwrite 할 수 있음
        today = timezone.localtime(timezone.now()).date()
        if today > value:
            raise serializers.ValidationError("Can't book in the past.")

        return value

    def validate(self, data):
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError("Check-in should be less than check-out")

        if Booking.objects.filter(
                check_in__lte=data["check_out"],
                check_out__gte=data["check_in"],
        ).exists():
            raise serializers.ValidationError("Those (or some) of those dates are already taken.")

        return data


class PublicBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )

