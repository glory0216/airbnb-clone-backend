from django.contrib import admin
from .models import Room, Amenity


## 특정 column의 값들을 초기화하거나, excel로 내보내기 등으로 사용할 때 유용
@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, queryset): ## model_admin, request, queryset 3개의 parameter는 필수
    for room in queryset.all():
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    actions = (reset_prices, )

    list_display = (
        "name",
        "price",
        "kind",
        "total_amenities",
        "rating",
        "owner",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "country",
        "city",
        "price",
        "rooms",
        "toilets",
        "pet_friendly",
        "kind",
        "amenities",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    search_fields = (
        "owner__username", ## contains
        "^name", ## ^: startswith
        "=price", ## =: exact
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",

    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )

