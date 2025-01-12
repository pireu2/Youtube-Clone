from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.paginator import Paginator
from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse

import json
import os
from moviepy import VideoFileClip
from datetime import datetime
from .models import User, Video, Comment, Like, Dislike, Subscription, Card, Wallet
from . import forms

# Create your views here.


def index(request):
    if request.method != "GET":
        return render(request, "app/error.html", {"message": "GET method required."})
    latest_vids = Video.objects.all()
    latest_vids = latest_vids.order_by("-timestamp")
    latest_vids = latest_vids[:3]
    if request.user.is_authenticated:
        sub_values = [
            sub.creator for sub in Subscription.objects.filter(subscriber=request.user)
        ]
        subbed_vids = Video.objects.filter(creator__in=sub_values)
        subbed_vids = subbed_vids[:3]
    else:
        subbed_vids = []
    return render(
        request,
        "app/index.html",
        {"latest_vids": latest_vids, "subbed_vids": subbed_vids},
    )


def latest(request):
    if request.method != "GET":
        return render(request, "app/error.html", {"message": "GET method required."})
    latest_vids = Video.objects.all()
    latest_vids = latest_vids.order_by("-timestamp")
    return render(request, "app/latest.html", {"latest_vids": latest_vids})


@login_required
def subscribed(request):
    if request.method != "GET":
        return render(request, "app/error.html", {"message": "GET method required."})
    sub_values = [
        sub.creator for sub in Subscription.objects.filter(subscriber=request.user)
    ]
    subbed_vids = Video.objects.filter(creator__in=sub_values)
    return render(request, "app/subscribed.html", {"subbed_vids": subbed_vids})


def login_view(request):
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        # Attempt to sign user in
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                form = forms.LoginForm()
                return render(
                    request,
                    "app/login.html",
                    {"message": "Invalid username or password", "form": form},
                )
    else:
        form = forms.LoginForm()
        return render(request, "app/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]

            # Ensure password matches confirmation
            password = form.cleaned_data["password"]
            confirmation = form.cleaned_data["confirmation"]
            if password != confirmation:
                form = forms.RegistrationForm()
                return render(
                    request,
                    "app/register.html",
                    {"message": "Passwords must match.", "form": form},
                )

            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                form = forms.RegistrationForm()
                return render(
                    request,
                    "app/register.html",
                    {"message": "Username already taken.", "form": form},
                )
            wallet = Wallet(user=user, balance=0)
            wallet.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        form = forms.RegistrationForm()
        return render(request, "app/register.html", {"form": form})


@login_required
def upload(request):
    if request.method == "POST":
        form = forms.VideoForm(request.POST, request.FILES)
        if form.is_valid():
            max_size = 250 * 1024 * 1024
            video_file = form.cleaned_data["video"]

            if video_file.size > max_size:
                form.add_error("video", "File size must be less than 250 MB.")
            else:
                title = form.cleaned_data["title"]
                description = form.cleaned_data["description"]
                timestamp = datetime.now()
                video = Video(
                    title=title,
                    creator=request.user,
                    description=description,
                    video=video_file,
                    timestamp=timestamp,
                )
                video.save()
                video.compress_video()


                return HttpResponseRedirect(reverse("watch", args=(video.id,)))
    else:
        form = forms.VideoForm()
        return render(request, "app/upload.html", {"form": form})


def watch(request, id):
    try:
        video = Video.objects.get(id=id)
    except Video.DoesNotExist:
        return render(
            request, "app/error.html", {"message": "This video does not exist"}
        )
    if request.method == "GET":
        if video:
            form = forms.CommentForm()
            comments = Comment.objects.filter(video=video).all()
            comments = comments.order_by("-timestamp")
            vids = Video.objects.exclude(id=id)[:20]
            liked = (
                Like.objects.filter(video=video, user=request.user).exists()
                if request.user.is_authenticated
                else False
            )
            disliked = (
                Dislike.objects.filter(video=video, user=request.user).exists()
                if request.user.is_authenticated
                else False
            )
            subbed = (
                Subscription.objects.filter(
                    creator=video.creator, subscriber=request.user
                ).exists()
                if request.user.is_authenticated
                else False
            )
            return render(
                request,
                "app/watch.html",
                {
                    "video": video,
                    "comments": comments,
                    "form": form,
                    "vids": vids,
                    "liked": liked,
                    "disliked": disliked,
                    "subbed": subbed,
                },
            )


@login_required
def like(request, video_id):
    if request.method != "POST":
        return render(request, "app/error.html", {"message": "POST method required."})
    video = Video.objects.get(id=video_id)
    try:
        like = Like.objects.get(video=video, user=request.user)
    except Like.DoesNotExist:
        video.likes += 1
        video.save()
        like = Like(video=video, user=request.user)
        like.save()
        return JsonResponse(
            {"message": "Like Success", "status": 200, "likes": video.likes}, status=200
        )
    else:
        video.likes = video.likes - 1
        video.save()
        like.delete()
        return JsonResponse(
            {"message": "Like Removed", "status": 200, "likes": video.likes}, status=200
        )


@login_required
def dislike(request, video_id):
    if request.method != "POST":
        return render(request, "app/error.html", {"message": "POST method required."})
    video = Video.objects.get(id=video_id)
    try:
        dislike = Dislike.objects.get(video=video, user=request.user)
    except Dislike.DoesNotExist:
        video.dislikes += 1
        video.save()
        dislike = Dislike(video=video, user=request.user)
        dislike.save()
        return JsonResponse(
            {"message": "disLike Success", "status": 200, "dislikes": video.dislikes},
            status=200,
        )
    else:
        video.dislikes = video.dislikes - 1
        video.save()
        dislike.delete()
        return JsonResponse(
            {"message": "disLike Removed", "status": 200, "dislikes": video.dislikes},
            status=200,
        )


@login_required
def subscribe(request, username):
    if request.method != "POST":
        return render(request, "app/error.html", {"message": "POST method required."})
    try:
        creator = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(
            request, "app/error.html", {"message": "This user does not exist."}
        )
    try:
        is_subbed = Subscription.objects.get(creator=creator, subscriber=request.user)
    except Subscription.DoesNotExist:
        sub = Subscription(creator=creator, subscriber=request.user)
        creator.subscribers += 1
        sub.save()
        creator.save()
        return JsonResponse(
            {"message": "Sub Success", "status": 200, "subs": creator.subscribers},
            status=200,
        )
    else:
        is_subbed.delete()
        creator.subscribers -= 1
        creator.save()
        return JsonResponse(
            {"message": "Unsub Success", "status": 200, "subs": creator.subscribers},
            status=200,
        )


@login_required
def comment(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    content = data.get("content")
    video_id = data.get("video_id")
    try:
        video = Video.objects.get(id=video_id)
    except Video.DoesNotExist:
        return JsonResponse({"error": "Video does not exitst"}, status=400)
    if content == "":
        return JsonResponse({"error": "Post requires content"}, status=400)
    timestamp = datetime.now()
    comment = Comment(
        video=video, content=content, user=request.user, timestamp=timestamp
    )
    comment.save()
    video.comments += 1
    video.save()
    formatted_datetime = timestamp.strftime("%b. %d, %Y, %I:%M %#p")
    return JsonResponse(
        {
            "message": "Post Success",
            "status": 200,
            "avatarurl": request.user.avatar.url,
            "timestamp": formatted_datetime,
            "comments": video.comments,
        },
        status=200,
    )


def profile(request, username):
    try:
        current_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, "app/error.html", {"message": "User does not exist"})
    try:
        has_card = True if Wallet.objects.get(user=request.user).card else False
    except Wallet.DoesNotExist:
        has_card = False
    videos = Video.objects.filter(creator=current_user)
    videos.order_by("-timestamp")
    subbed = (
        Subscription.objects.filter(
            creator=current_user, subscriber=request.user
        ).exists()
        if request.user.is_authenticated
        else False
    )
    return render(
        request,
        "app/profile.html",
        {
            "current_user": current_user,
            "videos": videos,
            "subbed": subbed,
            "has_card": has_card,
        },
    )


@login_required
def change(request):
    if request.method == "GET":
        form = forms.PicureForm()
        return render(request, "app/change.html", {"form": form})
    else:
        form = forms.PicureForm(request.POST, request.FILES)
        if form.is_valid():
            avatar = form.cleaned_data["avatar"]
            user = User.objects.get(username=request.user.username)
            user.avatar = avatar
            user.save()
            return HttpResponseRedirect(reverse("profile", args=(user.username,)))


@login_required
def add_funds(request):
    if request.method == "GET":
        try:
            Wallet.objects.get(user=request.user).card
        except Wallet.DoesNotExist:
            return render(
                request,
                "app/error.html",
                {"message": "You must have a card to add Funds."},
            )
        return render(request, "app/add_funds.html")
    else:
        amount = int(request.POST["amount"])
        wallet = Wallet.objects.get(user=request.user)
        wallet.balance += int(amount)
        wallet.save()
        return HttpResponseRedirect(reverse("profile", args=(request.user.username,)))


@login_required
def donate(request, username):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    if username == request.user.username:
        return render(
            request, "app/error.html", {"message": "Can't donate to yourself."}
        )
    current_user = User.objects.get(username=username)
    try:
        donator_wallet = Wallet.objects.get(user=request.user)
        wallet = Wallet.objects.get(user=current_user)
    except Wallet.DoesNotExist:
        return render(
            request, "app/error.html", {"message": "User does not have a wallet."}
        )

    amount = request.POST["amount"]
    amount = int(amount)
    if amount <= 0:
        return render(
            request, "app/error.html", {"message": "Can't negative ammounts!"}
        )
    if amount > donator_wallet.balance:
        return render(request, "app/error.html", {"message": "Insufficiend funds!"})

    donator_wallet.balance -= amount
    donator_wallet.save()
    wallet.balance += amount
    wallet.save()
    return HttpResponseRedirect(reverse("profile", args=(username,)))


@login_required
def add_card(request):
    has_wallet = Wallet.objects.filter(user=request.user).exists()
    try:
        has_card = True if Wallet.objects.get(user=request.user).card else False
    except Wallet.DoesNotExist:
        has_card = False
    if request.method == "GET":
        form = forms.CardForm()
        return render(
            request, "app/add_card.html", {"form": form, "has_card": has_card}
        )
    else:
        form = forms.CardForm(request.POST)
        if form.is_valid():
            card_number = str(form.cleaned_data["number"])
            expiration_date = form.cleaned_data["expiration_date"]
            cvv = str(form.cleaned_data["cvv"])

            if len(card_number) != 16:
                return render(
                    request, "app/error.html", {"message": "Invalid card number."}
                )
            if expiration_date < datetime.date(datetime.now()):
                return render(request, "app/error.html", {"message": "Card Expired."})
            if len(cvv) != 3:
                return render(
                    request, "app/error.html", {"message": "Invalid cvv number."}
                )

            card = Card(number=card_number, expiration_date=expiration_date, cvv=cvv)
            card.save()
            if not has_wallet:
                wallet = Wallet(card=card, user=request.user, balance=0)
                wallet.save()
            else:
                if not has_card:
                    wallet = Wallet.objects.get(user=request.user)
                    prev_card = wallet.card
                    wallet.card = card
                    wallet.save()
                    if prev_card:
                        prev_card.delete()

            return HttpResponseRedirect(
                reverse("profile", args=(request.user.username,))
            )


def search(request, input):

    if request.method != "GET":
        return render(request, "app/error.html", {"message": "GET method required."})
    videos = Video.objects.filter(title__icontains=input)
    videos = videos.order_by("-timestamp")
    return render(request, "app/search.html", {"videos": videos, "input": input})
