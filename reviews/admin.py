from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):
    title = "Filter by words"

    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, queryset):
        word = self.value() ## query param의 value
        if word:
            return queryset.filter(payload__contains=word)
        else:
            queryset


class GoodBadFilter(admin.SimpleListFilter):
    title = "Filter by bad/good reviews"

    parameter_name = "is_good_bad"

    FILTER_SET = dict(
        good="rating__gte",
        bad="rating__lt"
    )

    def lookups(self, request, model_admin):
        return [
            ("good", "Good Reviews"),
            ("bad", "Bad Reviews"),
        ]

    def queryset(self, request, queryset):
        select = self.value() ## query param의 value 가져오기
        if select:
            filter_set = {
                self.FILTER_SET[select]: 3
            }
            return queryset.filter(**filter_set)
        else:
            queryset


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "__str__",
        "payload"
    )

    list_filter = (
        GoodBadFilter,
        WordFilter,
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",
    )
