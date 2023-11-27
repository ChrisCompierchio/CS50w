
from django.urls import path

from . import views
from network.views import newLike

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:clickedUser>", views.profile, name="profile"),
    path("following", views.following, name="following"),

    path("unlike/<int:post_id>", views.unlike, name="unlike"),
    path("newLike/<int:post_id>", newLike, name="new_like"),
    path("posts/<int:post_id>", views.post, name="post"),
    path("likes", views.like, name="like"),
    path("newFollow/<int:clickedUserId>", views.newFollow, name="newFollow"),
    path("deleteFollow/<int:clickedUserId>", views.deleteFollow, name="deleteFollow")
]
