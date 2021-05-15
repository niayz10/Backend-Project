from django.shortcuts import render
import logging
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from auth_.models import CustomUser
from auth_.serializers import CustomUserSerializer, CustomUserSerializerAll
from auth_.permissions import AdminPermission, GuestPermission
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

logger = logging.getLogger(__name__)


class User(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def list_of_users(self, request):
        logger.info('list of a users')
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        logger.info('Registration of a user')
        email = request.data.get("email")
        password = request.data.get("password")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        avatar = request.data.get("avatar")
        user = CustomUser.objects.create_user(email, password, first_name=first_name, last_name=last_name,
                                              avatar=avatar)
        serializer = CustomUserSerializer(user, many=False)
        return Response(serializer.data)

    def get_permissions(self):
        logger.info('Profile of the current user')
        if self.action == 'create':
            permission_classes = [AdminPermission]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_information_about_yourself(self, request):
        logger.debug('Profile of the current user')
        print(request.user.is_anonymous)
        serializer = CustomUserSerializerAll(request.user, many=False)
        return Response(serializer.data)
