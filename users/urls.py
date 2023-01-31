from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("me", views.Me.as_view()),
    path("change-password", views.ChangePassword.as_view()),
    path("log-in", views.Login.as_view()),
    path("log-out", views.Logout.as_view()),
    path("@<str:username>", views.PublicUser.as_view()),
    path("@<str:username>/reviews", views.UserReviews.as_view()),
    path("@<str:username>/rooms", views.HostRooms.as_view()),
    path("@<str:username>/rooms/reviews", views.HostReviews.as_view()),
]

