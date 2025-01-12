from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("upload", views.upload, name="upload"),
    path("watch/<int:id>", views.watch, name="watch"),
    path("like/<int:video_id>", views.like, name="like"),
    path("dislike/<int:video_id>", views.dislike, name="dislike"),
    path("subscribe/<str:username>", views.subscribe, name="subscribe"),
    path("comment", views.comment, name="comment"),
    path("latest", views.latest, name="latest"),
    path("subscribed", views.subscribed, name="subscribed"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("change", views.change, name="change"),
    path("search/<str:input>", views.search, name="search"),
    path("add_card/", views.add_card, name="add_card"),
    path("add_funds/", views.add_funds, name="add_funds"),
    path("donate/<str:username>", views.donate, name="donate"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
