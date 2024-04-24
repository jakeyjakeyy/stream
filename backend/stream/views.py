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

        return Response({"isLive": stream.started_at is not None})


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
