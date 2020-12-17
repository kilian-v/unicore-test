import json
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .renderers import UserJSONRenderer
from .serializer import RegistrationSerializer, LoginSerializer
from rest_framework_api_key.models import APIKey
from .models import Place, User
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance


class RegistrationView(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    # @action(detail=True, renderer_classes=[UserJSONRenderer], methods=['post'])
    def register(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(viewsets.ModelViewSet):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def login(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiKeyView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def apikey(self, request):
        username = request.user.username
        public_key = APIKey.objects.get(name="public-key" + "-" + username)
        private_key = APIKey.objects.get(name="private-key" + "-" + username)

        return Response({
            public_key.name: public_key.id,

            private_key.name: private_key.id,
        })


class RestaurantsView(viewsets.ViewSet):

    def list(self, request):
        public_key = request.META["HTTP_X_PUBLIC_KEY"]
        private_key = request.META["HTTP_X_PRIVATE_KEY"]
        if len(public_key) != 87:
            return Response("Please enter a valid Public Key")
        if len(private_key) != 87:
            return Response("Please enter a valid Private Key")
        data = request.data
        lat = float(data["lat"])
        lng = float(data["lng"])
        point = Point(lng, lat)
        radius = 3
        places = Place.objects.filter(location__distance_lt=(point, Distance(km=radius))).values()
        return Response(str(places))