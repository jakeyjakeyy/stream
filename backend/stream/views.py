from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from stream import models
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404
import logging
from django.contrib.auth.models import User
from datetime import datetime
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)


@csrf_exempt
def start_stream(request):
    logger.info(f"Starting stream {request.POST}")

    stream = get_object_or_404(models.Stream, key=request.POST["name"])

    if stream.started_at:
        return HttpResponseForbidden({"Stream already started."})

    stream.started_at = timezone.now()
    stream.save()

    # redirection to public username
    return redirect("/" + stream.user.username)


@csrf_exempt
def stop_stream(request):
    stream = models.Stream.objects.get(key=request.POST["name"])

    stream.started_at = None
    stream.save()
    return HttpResponse("OK")


class UserStreamInfo(APIView):
    def get(self, request, username):
        stream = models.Stream.objects.filter(user__username=username).first()

        if not stream:
            return Response({"error": "Stream not found."}, status=404)

        return Response(
            {
                "isLive": stream.started_at is not None,
                "title": stream.title,
                "about": stream.about,
                "name": stream.user.username,
            }
        )


class Following(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        following = models.Follow.objects.filter(user=user)

        return Response(
            {
                "following": [
                    {
                        "username": f.target.username,
                        "isLive": f.target.stream.is_live,
                    }
                    for f in following
                ]
            },
            status=200,
        )


class Follow(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user
        target = User.objects.get(username=request.data.get("username"))
        follow = request.data.get("follow")
        if follow:
            models.Follow.objects.create(user=user, target=target)
        else:
            models.Follow.objects.filter(user=user, target=target).delete()

        return Response({"follow": follow}, status=200)


class Featured(APIView):
    def get(self, request):
        featured = models.Featured.objects.all()

        return Response(
            {
                "featured": [
                    {
                        "username": f.stream.user.username,
                        "is_live": f.stream.is_live,
                        "started_at": f.stream.started_at,
                        "about": f.stream.about,
                    }
                    for f in featured
                ]
            },
            status=200,
        )


class RegisterUser(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required."}, status=400)

        user = User.objects.create_user(username=username, password=password)
        return Response({"username": user.username}, status=201)


class WhoAmI(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        return Response({"username": request.user.username}, status=200)


class Update(APIView):  # Update elements of users stream
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user
        if request.data.get("title"):
            stream = models.Stream.objects.get(user=user)
            stream.title = request.data.get("title")
            stream.save()
            return Response({"title": stream.title}, status=200)
        if request.data.get("about"):
            stream = models.Stream.objects.get(user=user)
            stream.about = request.data.get("about")
            stream.save()
            return Response({"about": stream.about}, status=200)


class Subscribe(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user
        targetU = User.objects.get(username=request.data.get("target"))
        target = models.Stream.objects.get(user=targetU)
        subscribe = request.data.get("subscribe")
        if subscribe == True:
            now = datetime.now()
            one_month = now + relativedelta(months=1)
            models.Subscription.objects.create(
                user=user, stream=target, expires_at=one_month
            )
        elif subscribe == "check":
            sub = models.Subscription.objects.filter(user=user, stream=target).first()
            if sub:
                return Response(
                    {"subscribed": True, "expires": sub.expires_at, "renew": sub.renew},
                    status=200,
                )
            else:
                return Response({"subscribed": False}, status=200)
        elif subscribe == False:
            sub = models.Subscription.objects.get(user=user, stream=target)
            if request.data.get("renew"):
                sub.renew = True
                sub.save()
                return Response({"renew": True}, status=200)
            sub.renew = False
            sub.save()
            return Response({"renew": False}, status=200)

        return Response({"subscribe": subscribe}, status=200)
